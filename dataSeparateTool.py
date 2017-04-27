import re
import sys

###################
# 功能1：提取源代码中的字符串，并生成配置文件
# 若源代码中有多个字符串是相同的，则在配置文件中体现为不同的条目
# 
# 功能2：利用配置文件中的设置，对源代码中的字符串进行数据分离。
# 即使值相同，配置文件中的键也不能相同，若有相同的键，程序会进行提示。


#间接调用
#分析给定的代码文件，返回其中的非空字符串组成的list
def analyzeCodeFile(filename):
	fo=open(filename,encoding="utf-8")
	str=fo.read()
	fo.close()
	strs=re.findall(r'"(?:\\.|[^"\\\n])+?"',str)
	return strs

#提取代码中的字符串，生成配置文件
def generatePropFile(codeFilename,propFilename):
	strs=analyzeCodeFile(codeFilename)
	fo=open(propFilename,mode="w+",encoding="utf-8")
	for str in strs:
		tmpStr='='+str+"\n"
		fo.write(tmpStr)
	fo.close()
	


#间接调用
#分析配置文件，返回键与值的
def analyzePropFile(filename):
	fo=open(filename,encoding="utf-8")
	str=fo.read()
	fo.close()
	props=[]
	tmp2=[]
	for prop in str.split("\n"):
		if prop!="":
			props.append(prop.split("=",1))
	for tmp in props:
		if tmp[0]=='':
			print('exist empty key')
			exit(0)
		if tmp[0] in tmp2:
			print('some keys have same name')
			exit(0)
		tmp2.append(tmp[0])
	return props


#间接调用
#对 filename 中的数据进行替换
def propReplace(filename,props):
	fo=open(filename,mode="r+",encoding="utf-8")
	str=fo.read()
	for prop in props:
		oldStr=prop[1]
		newStr='prop.getProperty("{0}")'.format(prop[0])
		str=str.replace(oldStr,newStr,1)
	fo.seek(0)
	fo.write(str)
	fo.close()

#分析给定的数据文件，对代码文件进行数据分离
def dataSeparate(codeFilename,propFilename):
	props=analyzePropFile(propFilename)
	#print(props)
	propReplace(codeFilename,props)
	
	
if __name__=="__main__":
	helpMsg="""
使用说明：
	 可执行文件名 <Option> codeFile propFile
	 
	 Option:
	-g
		提取代码文件中的字符串，生成配置文件
	-r
		利用配置文件，对代码文件进行数据分离
		
	codeFile:
		代码文件的路径
		
	propFile:
		配置文件的路径
	"""
	if len(sys.argv)!=4 or sys.argv[1] not in ['-g','-r']:
		print(helpMsg)
		exit(0)
	
	#生成配置文件
	if sys.argv[1]=='-g':
		print("[生成配置文件]")
		print("源码文件："+sys.argv[2]+"\n配置文件："+sys.argv[3])
		generatePropFile(sys.argv[2],sys.argv[3])
	#进行数据分离
	elif sys.argv[1]=='-r':
		print("[进行数据分离]")
		print("源码文件："+sys.argv[2]+"\n配置文件："+sys.argv[3])
		dataSeparate(sys.argv[2],sys.argv[3])
	else:
		print("未知错误")
