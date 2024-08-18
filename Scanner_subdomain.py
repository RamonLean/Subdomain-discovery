import requests
import argparse
import threading

print("#####This is a brute force subdomain discovery scanner, be careful and be resposible for yor actions.####")

class subdomain_discovering:
    
    def __init__(self):

        '''This section initialize arguments and variables the will be used in all code'''
        
        print ("\n\nExample of usage: \npython3 Scanner_subdomain.py MYDOMAIN.COM -l list_subdomains.txt --save MYDISCOVERIES.txt \n\n")

        parser = argparse.ArgumentParser()
        parser.add_argument("DOMAIN", help="Enter the domain" "exemple.com" "")
        parser.add_argument("-l", "--list", help="File text with the subdomian list")
        parser.add_argument("--save",help="File to save the subdomians discovered")

        args = parser.parse_args()
        self.domain = args.DOMAIN
        self.subs_test= args.list
        self.save = args.save

    def open_the_file (self):
        
        '''Function to open the list of subdomains and return each line to the "processing" function'''
        
        try:
            file_ = open(self.subs_test)
            content = file_.read()
            subdomains = content.splitlines()
            
        except:
            print("\n\n\n\n\n\n-------------------------------Wordlist not found------------------------------------------------------\n\n\n\n")
            exit()

        #discoverd_subs = []
        for subdomain in subdomains:
            yield subdomain
        
        yield None
         
    def request_to_subdomains(self,subdomain):

        ''' This section is responsible to make the requests to the subdomains, 
        testing HTTPS and HTTP, but sometimes even 
        though the subdomain is discovered with HTTP (without TLS), all 
        traffic can be redirected to HTTPS due to load balancer/server 
        rule, i.e., just because a subdomain accepts an HTTP requests, it 
        doesn't mean that you will interact with it without TLS, but you can try.'''
        
        subdomain=subdomain
        
        url_httpS = f"https://{subdomain}.{self.domain}"
        url_http = f"http://{subdomain}.{self.domain}"
        
        try:
            requests.get(url_httpS,timeout=5)
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass
        else:
            print("[+] Subdomain discovered using HTTPS:", url_httpS)
            self.save_discoverd_to_file(url_httpS)

        try:
            requests.get(url_http,timeout=5)
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass

        else:
            print("[+] Subdomain discovered using HTTP only:", url_http)
            self.save_discoverd_to_file(url_http)

    def save_discoverd_to_file(self,url, subs_discovered='subs_discovered.txt'):
        '''Responsible to save the discoveries to file'''
        
        if ((self.save)==''):
            self.save='subs_discovered.txt'            
        
        with open(self.save, "a") as f:
            print(str(url), file=f)
        print(".......................New sub domain written to the file.........................")

    def processing(self,interator):
        
        ''' This function is passed as an argument to “threads_call” and is responsible for calling “request_to_subdomains”, which in turn makes the requests to the subdomains. '''
        
        while True:
            try:
                items0 = next(interator)
                while items0 is not None:
                    self.request_to_subdomains(items0)
                    items0 = next(interator)
                break
            except ValueError as error:
                    pass
                
    def threads_call(self,QTD_thread=10):

        ''' Thread function, you can define whatever you want but make sure o system has the necessary resources.'''
        
        threads_ = []
        interator = self.open_the_file()
        for ixt in range(QTD_thread):
            x1 = threading.Thread(target=self.processing, args=(interator,))
            threads_.append(x1)
            x1.start()

        for i in threads_:
            i.join()
            
if __name__ == '__main__':
    
       calling = subdomain_discovering()
       calling.threads_call()
