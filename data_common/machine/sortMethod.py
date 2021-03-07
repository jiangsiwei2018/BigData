# # -*- coding: utf-8 -*-
# """
# Created on Wed Jun 15 23:11:10 2016
#
# @author: Administrator
# """
# ###########################
# #冒泡法：对比模型，原数组上排序，稳定，慢
# #
# #插入法：对比模型，原数组上排序，稳定，慢
# #
# #选择法：对比模型，原数组上排序，稳定，慢
# #
# ####归并法：对比模型，非原数组上排序，稳定，快####(暂不予考虑)
# #
# #快速法：对比模型，原数组上排序，不稳定，快
#
# ###########################
# #只需要掌握四中常用排序算法
# #1.冒泡排序：循环，两两向后比较
# #2.选择排序：每次挑选数组的最值，与前置元素换位，然后继续挑选剩余元素的最值并重复操作
# #3.插入排序：顺序地从数组里获取数据，并在一个已经排序好的序列里，插入到对应的位置
# #4.快速排序：选取待排序数组中的一个元素，将数组中比这个元素大的元素作为一部分，
# #          而比这个元素小的元素作为另一部分，再将这两个部分和并
# ###########################
#
#
# #冒泡排序
# def bubbleSort(L):
#     assert(type(L)==type(['']))
#     length = len(L)
#     if length==0 or length==1:
#         return L
#     for i in xrange(length):
#         for j in xrange(length-1-i):
#             if L[j] < L[j+1]:
# #                temp = L[j]
# #                L[j] = L[j+1]
# #                L[j+1] = temp
#                 L[j],L[j+1]=L[j+1],L[j]
#     return L
#
# #选择排序
# def selectSort(L):
#     assert(type(L)==type(['']))
#     length = len(L)
#     if length==0 or length==1:
#         return L
#
#     def _max(s):
#         largest = s
#         for i in xrange(s,length):
#             if L[i] > L[largest]:
#                 largest = i
#         return largest
#
#     for i in xrange(length):
#         largest = _max(i)
#         if i!=largest:
#             temp = L[largest]
#             L[largest] = L[i]
#             L[i] = temp
#     return L
#
# #插入排序
# def insertSort(L):
#     assert(type(L)==type(['']))
#     length = len(L)
#     if length==0 or length==1:
#         return L
#     for i in xrange(1,length):
#         value = L[i]
#         j = i-1
#         while j>=0 and L[j]<value:
#             L[j+1] = L[j]
#             j-=1
#         L[j+1] = value
#     return L
#
# #分治排序
#     #合并排序
# def MergeSort(lists):
#     if len(lists) <= 1:
#         return lists
#     num = int( len(lists)/2 )
#     left = MergeSort(lists[:num])
#     right = MergeSort(lists[num:])
#     lists=Merge(left, right)
#     return lists
#
# def Merge(left,right):
#     r, l=0, 0
#     result=[]
#     while l<len(left) and r<len(right):
#         if left[l] < right[r]:
#             result.append(left[l])
#             l += 1
#         else:
#             result.append(right[r])
#             r += 1
#     result += right[r:]
#     result += left[l:]
#     return result
#
#
# ##分治排序
# #    #合并排序
# #def mergeSort(L,start,end):
# #    assert(type(L)==type(['']))
# #    length = len(L)
# #    if length==0 or length==1:
# #        return L
# #    def merge(L,s,m,e):
# #        left = L[s:m+1]
# #        right = L[m+1:e+1]
# #        while s<e:
# #            while(len(left)>0 and len(right)>0):
# #                if left[0]>right[0]:
# #                    L[s] = left.pop(0)
# #                else:
# #                    L[s] = right.pop(0)
# #                s+=1
# #            while(len(left)>0):
# #                L[s] = left.pop(0)
# #                s+=1
# #            while(len(right)>0):
# #                L[s] = right.pop(0)
# #                s+=1
# #            pass
# #
# #    if start<end:
# #        mid = int((start+end)/2)
# #        mergeSort(L,start,mid)
# #        mergeSort(L,mid+1,end)
# #        merge(L,start,mid,end)
# #
# #    return L
# #
#
#
# #快速排序：选取待排序数组中的一个元素，将数组中比这个元素大的元素作为一部分，
# #        而比这个元素小的元素作为另一部分，再将这两个部分和并
#     #快速排序
# def quickSortPython(l):
#     assert(type(l)==type(['']))
#     length = len(l)
#     if length==0 or length==1:
#         return l
#     if len(l)<=1:
#         return l
#     left = [i for i in l[1:] if i>l[0]]
#     right = [i for i in l[1:] if i<=l[0]]
#     return quickSortPython(left) +[l[0],]+ quickSortPython(right)
#
#
#
#
#
#
#
# #**************************************************************#
# def selectSort2(L):
#     assert(type(L)==type(['']))
#     length = len(L)
#     if length==0 or length==1:
#         return L
#
#     def _max(s):
#         largest = s
#         for i in xrange(s,length):
#             if L[i] > L[largest]:
#                 largest = i
#         return largest
#
#     for i in xrange(length):
#         largest = _max(i)
#         print "****largest number postition _max=%d,largestN=L[%d]=%d****"%(largest,largest,L[largest])
#         if i!=largest:
#             print "**%d**%d**"%(L[largest],L[i])
#             temp = L[largest]
#             L[largest] = L[i]
#             L[i] = temp
#             print "**%d**%d**"%(L[largest],L[i])
#             print "\n"
#     return L
#     pass
# def insertSort2(L):
#     assert(type(L)==type(['']))
#     length = len(L)
#     if length==0 or length==1:
#         return L
#     for i in xrange(1,length):
#         value = L[i]
#         print "****the choose number i=%d,value=L[%d]=%d****"%(i,i,L[i])
#         j = i-1
#
#         while j>=0 and L[j]<value:
#             L[j+1] = L[j]
#             print "*****while*****number j+1=%d, L[%d]=%d"%(j+1,j+1,L[j+1])
#             j-=1
#             print "j-=1 j=%d"%j
#         L[j+1] = value
#         print "****number j+1=%d, L[%d]=%d****"%(j+1,j+1,L[j+1])
#         print L
#         print "\n"
#
#     return L
#
#
#
#
#
#
#
#
#
#
#
# #def mergeSort2(L,start,end):
# #    assert(type(L)==type(['']))
# #    #end=len(L)-1
# #    length = len(L)
# #    if length==0 or length==1:
# #        return L
# #    #L适合已经排序好的序列（由两个已经排序的数列合并）
# #    def merge2(L,s,m,e):
# #        left = L[s:m+1]
# #        right = L[m+1:e+1]
# #        print "beginning left:"
# #        print left
# #        print "beginning right"
# #        print right
# #        while s<e:
# #            while(len(left)>0 and len(right)>0):
# #                if left[0]>right[0]:
# #                    L[s] = left.pop(0)
# #                    print "left:"
# #                    print left
# #                    print "L***"
# #                    print L
# #
# #                else:
# #                    L[s] = right.pop(0)
# #                    print "right"
# #                    print right
# #                    print "L---"
# #                    print L
# #
# #                s+=1
# #                print "------------------------------------------"
# #                print "          s=%d           "%s
# #            print "**********1*********"
# #            print L
# #            while(len(left)>0):
# #                L[s] = left.pop(0)
# #                s+=1
# #            while(len(right)>0):
# #                L[s] = right.pop(0)
# #                s+=1
# #            print "----------1----------"
# #            print L
# #            pass
# #
# ##    if start<end:
# ##        mid = int((start+end)/2)
# ##        mergeSort2(L,start,mid)
# ##        mergeSort2(L,mid+1,end)
# ##        merge2(L,start,mid,end)