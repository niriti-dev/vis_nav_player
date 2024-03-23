from vis_nav_game import Player, Action
import pygame
import cv2


class KeyboardPlayerPyGame(Player):
    def __init__(self):
        self.fpv = None
        self.screen = None
        self.keymap = None

        self.last_act = Action.IDLE
        self.last_start = 0  
        self.last_end = 0  

        self.key_log = [] 
        self.tutorial_mode = 0 


        # delete later 
        self.act_count = 0 
        
        super(KeyboardPlayerPyGame, self).__init__()

        

    def reset(self):
        self.fpv = None
        self.last_act = Action.IDLE
        self.screen = None

        pygame.init()

        self.keymap = {
            pygame.K_LEFT: Action.LEFT,
            pygame.K_RIGHT: Action.RIGHT,
            pygame.K_UP: Action.FORWARD,
            pygame.K_DOWN: Action.BACKWARD,
            pygame.K_SPACE: Action.CHECKIN,
            pygame.K_ESCAPE: Action.QUIT
        }

        self.key_map2 = {
            Action.LEFT:  pygame.K_LEFT, 
            Action.RIGHT:  pygame.K_RIGHT, 
            Action.FORWARD: pygame.K_UP, 
            Action.BACKWARD:  pygame.K_DOWN, 
            Action.CHECKIN:  pygame.K_SPACE, 
            Action.QUIT: pygame.K_ESCAPE
        }

    def act(self):
        print("in function")
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # click on the red window 
                pygame.quit()
                self.last_act = Action.QUIT
                return Action.QUIT

            # if self.tutorial_mode: 
            #     print("tutorial index: ", self.tutorial_idx)
            #     start, stuff, end  = self.key_log[self.tutorial_idx]
            #     end_act  = self.act_count + (end - start)
            #     print("end act: ", end_act)
            #     print("stuff: ", stuff)
                
            #     if self.tutorial_idx < len(self.key_log): 
            #         if self.act_count != end_act:
            #             print("stuff in numbers: ", self.key_map2[stuff])   
            #             # print(self.key_map2[stuff])   
            #             self.last_act = stuff            
            #             # self.last_act |= self.key_map2[stuff] # allows for continuous movement 

            #         else: 
            #             self.tutorial_idx +=1
            #             print("increasing")
            #             # print("tutorial mode: ", stuff)
            #         # event.type = pygame.KEYDOWN
            #     else: 
            #         self.tutorial_mode = False 
            #         event.type = pygame.K_SPACE

        
            if event.type == pygame.KEYDOWN:   
                print("keydown")
                print(event.key)

                
                if event.key == pygame.K_i: 
                    print('i key pressed, self.act: ', self.act_count)
                    self.tutorial_end = pygame.time.get_ticks() 
                    self.tutorial_mode = True; 
                    print("log length: ", len(self.key_log))
                    print("log\n", self.key_log)
                    # self.tutorial_mode= False  
                
                
                    
                if event.key in self.keymap:
                    print("VALID key in keymap")
                    # print(event.key)
                    print("act at this moment: ", self.act_count)


                    if not self.tutorial_mode: 
                        self.last_start = self.act_count
                        print("created self.last_start", self.last_start)
                        # event_shit = self.las
                        # # self.key_log.append((timestamp, event.key))
                        # self.key_log.append((timestamp, self.last_act))


                    self.last_act |= self.keymap[event.key] # allows for continuous movement 
                    # results in (ACTION.RIGHT | ACTION.LEFT) type shit 
                    print(self.last_act)

                    
                    # logging it in 
                    # also logs in the 'esc' so work on that later 
    

                else:
                    self.show_target_images()
            
           
            if event.type == pygame.KEYUP :
                print("keyup")
                print(event.key)
                print("act AT THIS MOMENT: ", self.act_count)

                # if self.tutorial_mode: 
                #     # print("HEREEE")
                #     self.last_act = 0 # remove the effect 
                #     self.tutorial_mode = False; 

                if event.key in self.keymap: 
                    print(event.key)
                    self.last_end = self.act_count  # Get current timestame 

                    self.key_log.append((self.last_start, self.last_act, self.last_end))
                    self.last_act ^= self.keymap[event.key] # remove the effect 

                    # print(self.last_act)

        # self.last_end +=1 
        self.act_count += 1
        print(self.act_count)
        return self.last_act

    def show_target_images(self):
        targets = self.get_target_images()
        if targets is None or len(targets) <= 0:
            return
        hor1 = cv2.hconcat(targets[:2])
        hor2 = cv2.hconcat(targets[2:])
        concat_img = cv2.vconcat([hor1, hor2])

        w, h = concat_img.shape[:2]
        
        color = (0, 0, 0)

        concat_img = cv2.line(concat_img, (int(h/2), 0), (int(h/2), w), color, 2)
        concat_img = cv2.line(concat_img, (0, int(w/2)), (h, int(w/2)), color, 2)

        w_offset = 25
        h_offset = 10
        font = cv2.FONT_HERSHEY_SIMPLEX
        line = cv2.LINE_AA
        size = 0.75
        stroke = 1

        cv2.putText(concat_img, 'Front View', (h_offset, w_offset), font, size, color, stroke, line)
        cv2.putText(concat_img, 'Left View', (int(h/2) + h_offset, w_offset), font, size, color, stroke, line)
        cv2.putText(concat_img, 'Back View', (h_offset, int(w/2) + w_offset), font, size, color, stroke, line)
        cv2.putText(concat_img, 'Right View', (int(h/2) + h_offset, int(w/2) + w_offset), font, size, color, stroke, line)

        cv2.imshow(f'KeyboardPlayer:target_images', concat_img)
        cv2.imwrite('target.jpg', concat_img)
        cv2.waitKey(1)

    def set_target_images(self, images):
        super(KeyboardPlayerPyGame, self).set_target_images(images)
        self.show_target_images()

    def pre_exploration(self):
        K = self.get_camera_intrinsic_matrix()
        print(f'K={K}')

    def pre_navigation(self) -> None:
        pass

    def see(self, fpv):
        if fpv is None or len(fpv.shape) < 3:
            return

        self.fpv = fpv

        if self.screen is None:
            h, w, _ = fpv.shape
            self.screen = pygame.display.set_mode((w, h))

        def convert_opencv_img_to_pygame(opencv_image):
            """
            Convert OpenCV images for Pygame.

            see https://blanktar.jp/blog/2016/01/pygame-draw-opencv-image.html
            """
            opencv_image = opencv_image[:, :, ::-1]  # BGR->RGB
            shape = opencv_image.shape[1::-1]  # (height,width,Number of colors) -> (width, height)
            pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')

            return pygame_image

        pygame.display.set_caption("KeyboardPlayer:fpv")
        rgb = convert_opencv_img_to_pygame(fpv)
        self.screen.blit(rgb, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename='vis_nav_player.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    import vis_nav_game as vng
    logging.info(f'player.py is using vis_nav_game {vng.core.__version__}')
    
    the_player=KeyboardPlayerPyGame()
    vng.play(the_player)
    print(the_player.key_log)