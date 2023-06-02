import math
from PyPDF2 import PdfFileReader, PdfFileWriter
from optparse import OptionParser
import sys
import os

__author__ = "Kuhn Xin"
__author_email__ = "kunlong.xin@outlook.com"

class Driver(object):

    def __init__(self,opt,in_file) -> None:
        self._opt = opt
        self._in_file = in_file
        
    def invoke(self):
        pdf_read = PdfFileReader(self._in_file)
        start_page = 0
        page_number = 0
        split_flag = False
        
        write_path = os.path.join(os.getcwd(),self._in_file.split(".")[0])
        
        try:
            num_pages = pdf_read.getNumPages()
        except:
            if pdf_read.getIsEncrypted():
                if self._opt.decrypt_pdf:
                    print(self._opt.decrypt_pdf)
                    pdf_read.decrypt(self._opt.decrypt_pdf)
                    write_pdf = PdfFileWriter()  
                    for i in range(pdf_read.getNumPages()):
                        write_pdf.addPage(pdf_read.getPage(i))
                    write_pdf.write(open(self._in_file,mode="wb"))
        else:
            num_pages = pdf_read.getNumPages()
            
        if self._opt.pdf_info:
            pdf_info = pdf_read.getDocumentInfo()
            for key,value in pdf_info.items():
                print(key+": "+str(value))

        if self._opt.start_page:
            start_page = int(self._opt.start_page)
            assert start_page < num_pages
            
            
        if self._opt.page_number:
            page_number = int(self._opt.page_number)
            assert page_number > 1
            split_flag = True
        
        if not os.path.exists(write_path):
            os.mkdir(write_path)
        
        if (True == split_flag):
            
            if(self._opt.all_page):
                
                split_counter = math.ceil( (num_pages - start_page) / page_number )

                print("split_counter : %d"%(split_counter))

                idx = 0
                for index in range(split_counter):
                    if ( (index + 1) == split_counter):
                        if(num_pages - idx < page_number):
                            self.split_page(pdf_read,start_page + idx,num_pages - idx,write_path)
                        else:
                            self.split_page(pdf_read,start_page + idx,page_number,write_path)
                    else:
                        self.split_page(pdf_read,start_page + idx,page_number,write_path)
                    idx += page_number

            else:
                self.split_page(pdf_read,start_page,page_number,write_path)
                
            print("split ok !")

    def split_page(self,pdf_info:PdfFileReader,start_page:int,split_count:int,path_write):
        
        assert isinstance(start_page,int) 
        assert isinstance(split_count,int) 

        pdf_write = PdfFileWriter()
        for index in range(split_count):
            pdf_write.addPage(pdf_info.getPage(index + start_page))
        file_name = self._in_file.split(".")[0] + "_{0}-{1}.pdf".format(start_page + 1 ,start_page+split_count)
        path = os.path.join(path_write,file_name)
        pdf_write.write(open(path,mode="wb"))



def main():

    parser = OptionParser(usage="split <pdf-file>, notice: 0 means: first page!")

    parser.add_option("-i","--info",dest="pdf_info", action="store_true",help="show pdf info")
    parser.add_option("-s","--start",dest="start_page", action="store",help="pdf split start page")
    parser.add_option("-n","--number",dest="page_number", action="store",help="pdf split number")
    parser.add_option("-a","--all",dest="all_page", action="store_true",help=" split all pages from start page to end page")
    parser.add_option("-d","--decrypt",dest="decrypt_pdf", action="store",help="decrypt pdf")
    
    opts, args = parser.parse_args()

    if len(args) != 1:
        sys.stderr.write("Error: one input pdf-file must be specified\n")
        sys.exit(1)       
    
    driver = Driver(opts,args[0])

    driver.invoke()
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
