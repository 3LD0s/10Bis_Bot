#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import platform
import time
import json
import random
from bin import constants
import sys


class Bot:
    try:
        def __init__(self):
            self.options = webdriver.ChromeOptions()
            self.options.add_argument(f"--user-data-dir={constants.CHROME_DATA_LOCATION[platform.system()]}")
            self.options.add_argument(f"--profile-directory=Default")
            self.browser = webdriver.Chrome(executable_path=f"{constants.CHROME_DRIVER_LOCATION[platform.system()]}", options=self.options)
            self.last_sent_message = ""
            self.loaded = False
            self.current_chat_name = None
            with open("./src/database/conversation.json", 'r', encoding='UTF - 8') as handle:
                self.conversation = json.loads(handle.read())
            with open("./src/database/poll_answers.json", 'r', encoding='UTF - 8') as handle:
                self.poll_answers = json.loads(handle.read())
            with open("./src/database/poll_questions.json", 'r', encoding='UTF - 8') as handle:
                self.poll_questions = json.loads(handle.read())
            with open("./src/database/poll_groups.json", "r", encoding="UTF - 8") as handle:
                self.poll_groups = json.loads(handle.read())
                
            self.poll_num_length = 10
            self.question = None
            self.finished_poll = None
        
        def write_to_poll_answers(self, poll_answers):
            with open("./src/database/poll_answers.json", 'w', encoding='UTF - 8') as handle:
                handle.write(json.dumps(poll_answers, ensure_ascii=False))
                
        
        def write_to_poll_questions(self, poll_questions):
            with open("./src/database/poll_questions.json", 'w', encoding='UTF - 8') as handle:
                handle.write(json.dumps(poll_questions, ensure_ascii=False))
        
        def write_to_poll_groups(self, poll_groups):
            with open("./whatsapp-bot/src/database/poll_groups.json", 'w', encoding='UTF - 8') as handle:
                handle.write(json.dumps(poll_groups, ensure_ascii=False))
        
        def open_browser(self):
            '''
            Opens up the web browser into whatsapp web
            '''
            self.browser.get("http://web.whatsapp.com/")


        
        def click_on_chat(self, chat_name: str):
            '''
            Click on the chat name of the givin parameter,
            if the page hasn't loaded it will wait before continuing
            else will click and return
            '''
            #NOTE: Write to click_on_chat that if it does not find the element, it searches it and then clicks.
            if self.loaded:
                try:
                    chat = self.browser.find_element_by_xpath(f'//span[@title="{chat_name}"]')
                    self.loaded = True
                    chat.click()
                    self.current_chat_name = chat_name
                except NoSuchElementException as e:
                    '''
                    If Whatsapp web in a chat,
                    Writes to the user a message that chat_name
                    can't be found
                    '''
                    print("No such chat name")
                    print(e)
                except Exception as e:
                    print(e)
                    
                
            while not(self.loaded):
                try:
                    chat = self.browser.find_element_by_xpath(f'//span[@title="{chat_name}"]')
                    self.loaded = True
                    chat.click()
                    self.current_chat_name = chat_name
                except NoSuchElementException:
                    '''
                    If Whatsapp web in a chat,
                    Writes to the user a message that chat_name
                    can't be found
                    NOTE: Sovle the problem if the user enters at first a wrong name!
                    '''
                    pass
                except Exception as e:
                    print(e)

        
        # def get_answers(self, chat_name: str):
        #     '''
        #     A prototype function for getting the poll results after sending a message
        #     Needs to set a full sending messages machinisim for getting the results
        #     '''
        #     self.click_on_chat(chat_name)
        #     try:
        #         messages = self.browser.find_elements_by_xpath('//div[@class="_1Gy50"]//span/span')
        #         starting_time = f"{str(datetime.today().strftime('%d/%m/%Y'))}-{str(datetime.today().strftime('%H:%M'))}"
        #         temp_database = {
        #             f"{starting_time}" : ""
        #         }
        #         temp_answers = []
        #         started = False
                
        #         for message in messages:
        #             full_message = ''.join(message.text)
        #             if full_message == self.last_sent_message:
        #                 started = True
        #                 continue
        #             if started:
        #                 temp_answers.append(full_message)
                
        #         temp_database[starting_time] = temp_answers
        #         try:
        #             self.poll_answers.update(temp_database)
        #             with open("src/database/poll_answers.json", 'w') as handle:
        #                 handle.write(json.dumps(self.poll_answers))
        #             print("Writed to the database successfully")
        #             print(self.poll_answers)
        #         except Exception as e:
        #             print("Error as accur", e)
                    
        #     except NoSuchElementException:
        #         pass
            
        
        def send_message(self, msg: str, chat_name=None):
            '''
            Sends a message to specific chat name of the given parameter, if the chat name
            is different from the last chat it will first click on that chat.
            with a msg body
            '''
            if chat_name is None:
                chat_name = self.current_chat_name
            if chat_name != self.current_chat_name:
                self.click_on_chat(chat_name)
            text_box = self.browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
            text_box.click()
            time.sleep(.2)
            if "TAB" in msg:
                splited_message = msg.split("TAB ")
                text_box.send_keys(splited_message[0])
                ActionChains(self.browser).key_down(Keys.TAB).key_up(Keys.TAB).perform()
                msg_with_new_line = splited_message[1].split("\n")
            else:
                msg_with_new_line = msg.split("\n")
            for message in msg_with_new_line:
                    text_box.send_keys(message)
                    ActionChains(self.browser).key_down(Keys.CONTROL).key_down(Keys.ENTER).key_up(Keys.CONTROL).key_up(Keys.ENTER).perform()
            
            text_box.send_keys(Keys.ENTER)
            time.sleep(.2)
            self.last_sent_message = msg

        
        def get_last_answer(self):
            '''
            NOTE: Modify the function to return a list of message from the last message send by the bot to know
            whether there is more then one answer by the client
            And add the fuction to know whether we talk in a group chat or individual
            '''
            while True:
                time.sleep(2)
                messages = self.browser.find_elements_by_xpath('//div[@class="_1Gy50"]//span/span')
                if ''.join(messages[-1].text) != self.last_sent_message:
                    return ''.join(messages[-1].text)        
            
            
        # def start_conversation(self, chat_name):
        #     self.send_message(msg=self.last_sent_message, chat_name=chat_name)
        #     self.send_message(msg="תשאל אותי אחת מן האפשרויות הבאות בלבד עד שתגיד לי די", chat_name=chat_name)
        #     self.send_message(msg='\n'.join(self.conversation['questions']), chat_name=chat_name)
        #     user_answer = self.get_last_answer()
        #     while user_answer != "די":
        #         try:
        #             answer_index = self.conversation['questions'].index(user_answer)
        #             self.send_message(msg=self.conversation['answers'][answer_index], chat_name=chat_name) 
        #             user_answer = self.get_last_answer()
        #         except ValueError as e:
        #             self.send_message(msg="תבחר בבקשה מהאפשרויות שאמרתי לך", chat_name=chat_name)
        #             user_answer = self.get_last_answer()
        #             print(e)
        #     self.send_message(msg="טוב הפסקתי להתראות", chat_name=chat_name)
        
        
        def start_poll(self, chat_name):
            '''
            Starts the poll, as a param - chat name to click on.
            new_customer - initialaziדng a new poll and starts a conversation
            not_ready - When a user enters a not ready answer restart the chat
            poll_question - gets from the user poll question
            '''
            def new_customer():      
                self.send_message(self.conversation['q-new_customer'], chat_name=chat_name)
                answer = self.get_last_answer()
                try:
                    if answer == self.conversation['possible_answers'][0]:
                        poll_question()
                    else:
                        not_ready()
                except Exception as e:
                    print(e)
                    
            def not_ready():
                self.send_message(self.conversation['q-not_ready'])
                answer = self.get_last_answer()
                try:
                    if answer == self.conversation["possible_answers"][0]:
                        poll_question()
                    else:
                        new_customer()
                except Exception as e:
                    print(e)
                    
            def poll_question():
                self.send_message(self.conversation['q-poll_questions'])
                try:
                    if self.poll_questions[chat_name]:        
                        self.poll_questions[chat_name].append({'poll_question' : self.get_last_answer()})
                except KeyError as e:
                    self.poll_questions[chat_name] = [{'poll_question' : self.get_last_answer()}]
                    
                self.question = self.poll_questions[chat_name][-1]['poll_question']
                if self.question[-1] != "?":
                    self.question += '?'
                self.write_to_poll_questions(self.poll_questions)
                question_confirmation()
                
            def question_confirmation():
                self.send_message(self.conversation['q-question_confirmation'].replace('__', self.question))
                answer = self.get_last_answer()
                if answer == self.conversation['possible_answers'][0]:
                    num_of_answers()
                elif answer == self.conversation['possible_answers'][1]:
                    poll_question()
                else:
                    question_confirmation()
                
            def num_of_answers():
                self.send_message(self.conversation['q-num_of_answers'])
                answer = self.get_last_answer()
                try:
                    answers_number = int(answer)
                    if (answers_number > 1) and (answers_number < 9):
                        building_answers(answers_number)
                    else:
                        wrong_num_of_answers()
                        
                except ValueError as e:
                    wrong_num_of_answers()
                    
                except Exception as e:
                    print(e)
                    
                        
            def wrong_num_of_answers():
                self.send_message(self.conversation['q-wrong_num_answers'])
                num_of_answers()
            
            def building_answers(answers_number: int):
                self.send_message(self.conversation['q-explanation_of_answers'])
                self.send_message(self.conversation['q-explanation_of_answers_2'])
                user_answers = []
                for num in range(1, answers_number+1):
                    self.send_message(self.conversation['q-building_answers_{}'.format(num)])
                    user_answers.append(self.get_last_answer())
                self.poll_answers[self.question] = [f"{i+1}. {temp_answer}" for i, temp_answer in enumerate(user_answers)]
                self.write_to_poll_answers(self.poll_answers)
                poll_confirmation()
            
            def poll_confirmation():
                print(self.poll_answers[self.question])
                all_answers = ''.join([f"{answer}\n" for answer in self.poll_answers[self.question]]).strip()
                print(all_answers)
                self.finished_poll = self.conversation['q-poll_confirmation_1'].replace("__", f"{self.question}\n{all_answers}")
                self.send_message(self.finished_poll)
                self.send_message(self.conversation['q-poll_confirmation_2'])
                answer = self.get_last_answer()
                try:
                    if answer == self.conversation['possible_answers'][0]: 
                        self.send_message(self.conversation['a-poll_finished'])
                        self.send_message(self.conversation['a-poll_finished_2'])
                        poll_id = self.generate_guid()
                        send_poll_id_message = self.conversation['uuid_send'].replace("__", poll_id)
                        self.send_message(send_poll_id_message)
                        self.poll_questions[chat_name][-1].update({'poll_id' : poll_id})
                        # self.poll_questions[poll_question] = {'chat_name' : self.current_chat_name}
                        self.write_to_poll_questions(self.poll_questions)
                        self.search_poll_id() # Starts searching for the chat name by poll id
                    else:
                        self.send_message(self.conversation['a-poll_not_ready'])
                        answer = self.get_last_answer()
                        if answer == self.conversation['possible_answers'][0]:
                            poll_question()
                        elif answer == self.conversation['possible_answers'][1]:
                            num_of_answers()
                        else:
                            poll_confirmation()
                except Exception as e:
                    print(f"error: {e}")
                    pass
            
            new_customer()
                
        
        def generate_guid(self):
            poll_id = ''.join(["{}".format(random.randint(0, 9)) for self.poll_num_length in range(0, self.poll_num_length)])
            return poll_id    
        
        
        def search_poll_id(self):
            '''
            Searches in all whatsapp messages by the poll "id message"
            and refresh the page every 10s
            clicks the `x` button the refresh
            '''
            
            while True:
                try:
                    search_bar = self.browser.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
                    search_bar.click()
                    search_bar.send_keys("התחל סקר מספר ")
                    break
                except NoSuchElementException:
                    pass
                except Exception as e:
                    pass 
            try:
                time.sleep(10)                
                chats_search = self.browser.find_elements_by_xpath('//span[@class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr"]')
                if len(chats_search) >= 3:            
                    found_matching_poll_uuid = self.find_existing_poll_uuid(chats_search)
                    if found_matching_poll_uuid:
                        self.handle_poll_ids(found_matching_poll_uuid)
                    else:
                        self.search_again()
                else:
                    self.search_again()
                
            except NoSuchElementException:
                self.search_again()
        
            except Exception:
                self.search_again()
    
                    
        def search_again(self):
            while True:
                try:
                    exit_search_button = self.browser.find_element_by_xpath('//*[@id="side"]/div[1]/div/span/button')
                    exit_search_button.click()
                    time.sleep(10)
                    self.search_poll_id()
                    break
                except NoSuchElementException:
                    pass
                except Exception as e:
                    pass
                            
        
        def find_existing_poll_uuid(self, chats_search):
            print("Got in exisiting uuid")
            existing_uuids_found = {}
            def filter_errors(chats_search):
                new_chats = []
                for chat in chats_search:
                    try:
                        if chat.text:
                            new_chats.append(chat)
                    except Exception as e:
                        continue
                return new_chats
            
            new_chats = filter_errors(chats_search)
            for i, chat in enumerate(new_chats):
                try:
                    if i % 2 == 1:
                        found_uuid = re.findall(r" ([0-9]+)$", chat.text)[0]
                        user_names = self.poll_questions.keys()
                        for username in self.poll_questions:
                            if new_chats[i-1].text in user_names:
                                continue
                            for poll in self.poll_questions[username]:
                                if found_uuid == self.poll_questions[username][poll]['poll_id']:
                                    existing_uuids_found[new_chats[i-1].text] = found_uuid
                except Exception:
                    continue
            print(existing_uuids_found)
            return existing_uuids_found
            
        
        def handle_poll_ids(self, chats_search):     
            for group_name in chats_search:
                self.handle_poll_status(group_name, chats_search[group_name])
                
        
        def handle_poll_status(self, group_name, poll_id):
            
                
            def new_group(group_name, poll_id):
                #creates new group and new poll in poll_groups.json
                self.poll_groups[group_name] = [{"poll_id" : poll_id, "status" : "during poll"}]
                self.write_to_poll_groups()
                self.start_poll_in_group(group_name, poll_id)
                
            
            def new_poll(group_name, poll_id):
                #finds the group and enter the new poll in poll_groups.json
                self.poll_groups[group_name].append({"poll_id" : poll_id, "status" : "during poll"})
                self.start_poll_in_group(group_name, poll_id)
                
            
            def start_the_poll_again(group_name, poll_id):
                #finds the group and poll id and sets the status to suring poll
                for poll in self.poll_groups[group_name]:
                    if poll_id == self.poll_groups[group_name][poll]['poll_id']:
                        self.poll_groups[group_name][poll]["status"] = "during poll"
                self.start_poll_in_group(group_name, poll_id)
                

            def during_a_poll(group_name, poll_id):
                #sends the group a message saying they are already in the middle of a poll
                self.click_on_chat(group_name)
                self.send_message(self.conversation['during_poll'])
                pass
            
            try:
                if self.poll_groups[group_name]:
                    try:
                        if self.poll_groups[group_name][poll_id]:
                            if self.poll_groups[group_name][poll_id]['status'] == "finished":
                                start_the_poll_again(group_name, poll_id)
                            else:
                                during_a_poll(group_name, poll_id)
                    except KeyError:
                        new_poll(group_name, poll_id)
            except KeyError:
                new_group(group_name, poll_id)
            
        def start_poll_in_group(self, group_name, poll_id):
            self.click_on_chat(group_name)
            #NOTE: Write to click_on_chat that if it does not find the element, it searches it and then clicks.
            for username in self.poll_questions:
                if self.poll_questions[username]["poll_id"] == poll_id:
                    creator_username = username
                    break
            self.send_message(self.conversation['explanation_to_group_of_the_poll'].replace("__", f"@{creator_username}TAB"))
            self.send_message(self.finished_poll)
            
            
            
            
        # def convert_to_group_id(self, existing_uuids_found):
        #     groups_requested_polls = {}
        #     for group_name in existing_uuids_found.keys():
        #         self.click_on_chat(group_name)
        #         group_img_button = self.browser.find_element_by_xpath('//*[@id="main"]/header/div[1]/div/div') #needs to check if it actually clicks
        #         group_img_button.click() #needs to check if it actually clicks
        #         group_id = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[2]/div[2]').text #_3Bg5b VWPRY _1lF7t
        #         groups_requested_polls[group_id] = group_name
        #     return groups_requested_polls
    except Exception as e:
        print(f"Line Error: {sys.exc_info()[-1].tb_lineno}")
        
