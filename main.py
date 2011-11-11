# -*- coding:utf-8 -*-

# Name: main.py
# Author: Rehtal
# Date: 2011.11.8
# Version: 0.10
# Appendix: 0.10 version only collect book infomation.
# Description:
# This small program is used for judging douban user
# by his or her history record.
#
# For instance:
# 	One user used to read TAOCP and CLRS and make 
# 	some comments to the two books. Each of the two
# 	books has a weight(TAOCP:9.5 point and CLRS:9 point) 
# 	in background database. We can simply use a 
# 	fomula(first version use plus) to compute the user's 
# 	score(in this example the user get 18.5 point, in final
# 	edition we hope we can use 100 point as the full marks). 
#
# Finally we can give out a estimate score.
#
# In later edition we can use "machine learning"/"neural networks"
# or other techniques to resize weights saved in background database.

from extractHistoryInfo import extractHistoryInfo as ehf

if __name__ == '__main__':
	"""Current version doesn't use douban api
	only use normal html request to get user history records
	SLOW and STUPID! but can work."""
	userId = raw_input('User ID:')	
	e = ehf(userId)
	e.feed()
	e.smartPrint()
