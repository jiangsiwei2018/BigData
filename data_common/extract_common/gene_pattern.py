# coding=utf-8
import jieba


class GenePattern:

    def __init__(self):
        self.is_same_vector_flag = True
        self.is_same_prefix_flag = True
        self.domain_end_pos = 0
        self.last_delimiter = ''
        self.delimiter = '?'

    @staticmethod
    def cut_words(s, split=None):
        if not split:
            words = list(jieba.cut(s))
        else:
            if split == '/':
                _len = len(s.strip('/').split(split))
                words = s.split(split, _len -1)
            else:
                words = s.split(split)
        return words

    def is_same_vector(self, words):
        all_length = 0
        split_length = 0
        self.is_same_vector_flag = True
        self.is_same_prefix_flag = True
        for word in words:
            word = word.split(self.delimiter)[0].split('//')[-1]
            if not all_length and not split_length:
                all_length = len(self.cut_words(word))
                split_length = len(self.cut_words(word, '/'))
                continue
            v_b = all_length != len(self.cut_words(word))
            i_b = split_length != len(self.cut_words(word, '/'))
            if v_b or i_b:
                self.is_same_vector_flag = False
                if i_b:
                    print(f'words split by "/", but is not equal: {words}')
                    self.is_same_prefix_flag = False
                break

    def gene_pattern(self, urls):
        if not urls:
            return ''
        urls = urls if isinstance(urls, list) else [urls]
        if len(urls) == 1:
            domain = urls[0].split('//')[-1].split('/')[0]
            return f'https?://{domain}/.*'
        self.delimiter = '#' if '#' in urls[0] else '?'
        self.last_delimiter = '/' if urls[0].endswith('/') else '[^/]$'
        self.is_same_vector(urls)
        vectors = self.gene_vectors(urls)
        prefix_vectors = [vector[0] for vector in vectors]
        suffix_vectors = [vector[1] for vector in vectors]
        prefix_pattern = self.gene_prefix_pattern(prefix_vectors)
        suffix_pattern = self.gene_params_pattern(suffix_vectors)

        delimiter = '' if not suffix_pattern else f'\{self.delimiter}'
        return f'https?://{prefix_pattern}{self.last_delimiter}{delimiter}{suffix_pattern}'

    def gene_vectors(self, urls):
        vectors = []
        for url in urls:
            url_split = url.split(self.delimiter)
            # ? 后部分
            if len(url_split) == 1:
                all_prefix, all_suffix = url_split[0], ''
                params = []
            else:
                all_prefix, all_suffix = url_split[0], url_split[1]
                params = [item.split('=') for item in all_suffix.split('&')]
            # ?前部分
            prefix = all_prefix.split('//')[-1]
            if self.is_same_vector_flag and self.is_same_prefix_flag:
                words = self.cut_words(prefix)
            else:
                prefix_vector = self.cut_words(prefix, split='/')
                prefix_words = self.cut_words(prefix_vector[0], split='.')
                self.domain_end_pos = len(prefix_words)
                # if self.is_same_prefix_flag:
                words = prefix_words + prefix_vector[1:]
                # else:
                #     words = prefix_words + ['.*']
            vectors.append((words, params))
        return vectors

    def gene_prefix_pattern(self, vectors):
        words_cut_map = {}
        for words in vectors:
            for index, word in enumerate(words):
                if index not in words_cut_map:
                    words_cut_map[index] = []
                words_cut_map[index].append(word)

        pattern_items = []
        # 非紧邻位置的单一词更多的可能是'/' split不一致导致, 后面部分使用.*匹配就好
        index_same_part = -1
        len_max = 0
        for index, vector in words_cut_map.items():
            if len_max < len(vector):
                len_max = len(vector)
            if len(set(vector)) == 1:
                if index - index_same_part == 1 \
                        or vector[0] in ['.', '-', '+', '/', '&', '#']:
                    pattern_items.append(vector[0])
                    index_same_part = index
                else:
                    pattern_items.pop()
                    pattern_items.append('__all__')
                    self.last_delimiter = ''
                    break
            else:
                if index <= self.domain_end_pos:
                    index_same_part = index
                pattern_items.append('[^/]+')

        escape = ['.', '-', '+', '=', '?', '(', ')']
        pattern_items = [f'\\{word}' if word in escape else word
                         for word in pattern_items]

        if self.is_same_vector_flag:
            prefix_pattern = ''.join(pattern_items)
        else:
            domain = pattern_items[:self.domain_end_pos]
            suffix = pattern_items[self.domain_end_pos:]
            prefix_pattern = '\\.'.join(domain) + '/' + '/'.join(suffix)
        return prefix_pattern.replace('__all__', '.*')

    def gene_params_pattern(self, vectors):
        if not self.is_same_prefix_flag:
            return ''
        params_dict = {}
        for vector in vectors:
            if not vector:
                return ''
            for k, v in vector:
                if k not in params_dict:
                    params_dict[k] = []
                params_dict[k].append(v)
        params_list = []
        for k, v_vector in params_dict.items():
            if len(v_vector) >= 2 and len(set(v_vector)) == 1:
                s = f'{k}={v_vector[0]}'
            else:
                s = f'{k}=[^\\=&]+'
            params_list.append(s)
        return '&'.join(params_list)


if __name__ == '__main__':
    import re
    urls1 = [
        'https://www.cnblogs.com/satansz/p/12903262-aaa-222/aaaa',
        'https://sss.cnblogs.com/satansz/p/12905895-kkk/aaaa'
    ]
    p = GenePattern().gene_pattern(urls1)
    print(p)
    for url in urls1:
        flag = True if re.search(p, url) else False
        print(flag, url)

