from bs4 import BeautifulSoup
import requests
import time

class MyClass:

    def __init__ (self, patches, classes):
        self.version_patches = patches
        self.target_classes = classes


    def __get_html (self,version):

        url = f"https://liquipedia.net/dota2/Version_{version}"
        resp = requests.get(url)
        html_content = resp.content
        return url,BeautifulSoup(html_content,'html.parser')


    # def check_patch(self):
    #     for version in self.version_patches:
     
    #         url, soup = self.__get_html(version)
    #         p_tag = soup.find('p')

    #         if p_tag:
    #             p_text = p_tag.text.strip()

    #             if "There is currently no" in p_text:
    #                 print (f"ERROR: {url}",False)
    #             else:
    #                 print (f"SUCCESS: {url}",True)
    #         #else:
    #          #   print("CRITICAL ERROR: Tag specifier <p> has not been detected by bs4. The website structure might have been changed. Please recheck the HTML structure!")
       

    def __extract_data (self,version):

        # 7.31
        patch_information=[]

        ctr_entity=0
        ctr_phrases=0

        _,soup = self.__get_html(version)
        
        hero_start = soup.find('span',id='Heroes')

        all_h3 = hero_start.find_all_next('h3')
 
        for i,h3 in enumerate(all_h3):
            
            if (h3.find_next('ul')):

                ctr_entity+=1

                patch_information.append(h3.text.strip())

                ul_container = h3.find_next('ul')
                all_li = ul_container.find_all('li')

                for i,li in enumerate(all_li):
            
                    in_line = li.find('b')

                    if (in_line):
                        patch_information.append(in_line.text.strip())
                
                    else:
                        patch_class = li.find('img',alt=lambda value: value in self.target_classes)
                        if (patch_class):
                            patch_information.append(patch_class.get('alt') + " " + li.text.strip())

                            ctr_phrases+=1
            


        return ctr_entity,ctr_phrases,patch_information
    
    

    def build_data (self,save=False,verbose=0):
        ctr_en=0
        ctr_ph=0

        start_time = time.time()
        for version in self.version_patches:

            
            ctr_entity,ctr_phrases,patch_information = self.__extract_data(version)       
            ctr_en+= ctr_entity
            ctr_ph+=ctr_phrases

            if save:
                with open(f"text/{version}.txt",'a') as f:
                    for word in patch_information:
                        f.write(word+"\n")

                    f.write("\n")

            end_time = time.time()
     
            if verbose == 0:
                print("Build Dataset Success.\n")
            elif verbose == 2:
                for words in patch_information:
                    print(words)
            elif verbose == 1:
                run_time = end_time - start_time
                print("------------------------------")
                print(f"Version: {version}")
                print(f"Entities: {ctr_entity}")
                print(f"Phrases: {ctr_phrases}")
                print(f"Parse Time: {run_time}")
                print("------------------------------")
        
          
        
        
    
   


classes = ['Buff',"Nerf","New","Rework","Rescale","Removed"]
patches = ["7.31","7.32","7.35"]


obj = MyClass(patches,classes)
obj.build_data(True,2)


