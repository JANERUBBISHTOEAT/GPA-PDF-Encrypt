import PyPDF2 #可从PDF文档提取信息
import os #用于获取需要合并的PDF文件所在路径
from os.path import join, dirname
import hashlib

# Constants
SEPARATOR = "	"

# Global
cnt = 0
name_List = []
mail_List = []
sent_List = [] # MD5


def open_record():
    global cnt
    global name_List
    global mail_List
    global sent_List

    print("----------------------------")
    print("Reading records from in.txt:")
    
    try: 
        fp = open(join(dirname(__file__),"in.txt"), mode = 'r', encoding = 'UTF-8')
    except:
        print("[ERROR] Cannot find file: "+ join(dirname(__file__),"res.txt"))
        input()
        return False
    # "Check#Code#Name"
    text = fp.read()
    # print(text)
    for line in text.split('\n'):
        if SEPARATOR in line:
            sent_List.append(line.split(SEPARATOR)[0])
            mail_List.append(line.split(SEPARATOR)[2])
            name_List.append(line.split(SEPARATOR)[1].strip('\n').strip())
            if (sent_List[cnt]):
                print("|-√- " + mail_List[cnt] + '|' + name_List[cnt])
            else:
                print("|--- " + mail_List[cnt] + '|' + name_List[cnt])
            cnt += 1
        else:
            print("Unexpected Format Detected")
    fp.close()
    print(str(len(name_List)) + " records read sucesfully.")
    print("-----------------------\n")
    return True

def encrypt_pdf():
    cnt_loc = 0
    for name in name_List:
        print("Encrypting: " + name + ".pdf")
        pdf_reader = PyPDF2.PdfFileReader(open(join(dirname(__file__),"in.pdf"), "rb"))
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))
        md_5 = hashlib.md5((name + str(cnt_loc)).encode(encoding='UTF-8')).hexdigest()
        pdf_writer.encrypt(md_5)
        sent_List[cnt_loc] = md_5
        
        fp = open(join(dirname(__file__),"out.txt"), mode = 'w', encoding = 'UTF-8')
        for i in range(cnt):
            fp.write(sent_List[i] + SEPARATOR + name_List[i] + SEPARATOR + mail_List[i] + '\n')

        with open(join(dirname(__file__), "./out", name + ".pdf"), "wb") as f:
            pdf_writer.write(f)
        cnt_loc += 1
        

if __name__ == "__main__":
    open_record()
    encrypt_pdf()
