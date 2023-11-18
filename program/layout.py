'''
Classes in this file pertain to the structure of the user interface; game-specific
event listeners are not contained here.
'''

import copy
import pygame
from pygame import font
from globals import BLACK
font.init()

class Container:
  class Element:
    def __init__(self, content, parent=None, id=None):
      self.content = content # content is the surface or container
      self.id = id
      self.parent = parent
      self._offset = [0,0]
      self._absolute_offset = [0,0]
    
    @property
    def offset(self):
      return self._offset
    
    @property
    def vertical_offset(self):
       return self._offset[1]
    
    @vertical_offset.setter
    def vertical_offset(self, value):
       self._offset[1] = value
    
    @property
    def horizontal_offset(self):
       return self._offset[0]
    
    @horizontal_offset.setter
    def horizontal_offset(self,value):
       self._offset[0] = value
    
    @offset.setter
    def offset(self, value):
       self._offset = value

    @property
    def absolute_offset(self):
      parent = self.parent
      absolute_offset = [0,0]
      while parent is not None:
        absolute_offset[0] += parent.content.margin_left
        absolute_offset[1] += parent.content.margin_top
        parent = parent.parent
      return absolute_offset

    
    @absolute_offset.setter
    def absolute_offset(self, value):
       self._absolute_offset = value
     
  

  def __init__(self,parent, min_height=0,min_width=0, positioning='GROUPED', margin=(0,0,0,0),fill_color=BLACK):
    super(Container,self).__init__()
    # self.parent = None
    self.children = [] 
    self.fill_color=fill_color
    self.min_height = min_height
    self.min_width = min_width
    self.positioning = positioning
    self.parent = parent
    self.element = Container.Element(self)

    # set margin
    self.margin_top = margin[0]
    self.margin_left = margin[1]
    self.margin_bottom = margin[2]
    self.margin_right = margin[3]
    
    # set parent surface
    if isinstance(self.parent,pygame.Surface):
       self.parent_surface = parent
    elif isinstance(self.parent,Container):
       self.parent_surface = self.parent.surface

    # set surface
    if margin == (0,0,0,0): # if margin is not set assume 'flex' mode (see note above)
       sub_surface_height = min_height
       sub_surface_width = min_width
    elif not margin==(0,0,0,0):  
        sub_surface_width = self.parent_surface.get_width() - (self.margin_right + self.margin_left)
        sub_surface_height = self.parent_surface.get_height() - (self.margin_top + self.margin_bottom)
    self.surface = pygame.Surface((sub_surface_width, sub_surface_height))
    
    # set rect
    self.rect = self.surface.get_rect()  

  def _get_child_height(self, child):
     if isinstance(child, Container):
        return child.min_height
     elif isinstance(child,pygame.Surface):
        return child.get_rect().height
     
  def _get_child_width(self, child):
     if isinstance(child, Container):
        return child.min_width
     elif isinstance(child,pygame.Surface):
        return child.get_rect().width
  
  def _get_child_centery(self,child):
     if isinstance(child, Container):
        return child.get_rect().centery
     elif isinstance(child,pygame.Surface):
        return child.get_rect().centery
     
  def _get_child_centerx(self,child):
     if isinstance(child, Container):
        return child.get_rect().centerx
     elif isinstance(child,pygame.Surface):
        return child.get_rect().centerx

  def _blit_child_parent_surface(self, child, child_rect):
    if isinstance(child, Container):
      child_surface = pygame.Surface((child.get_width(),child.get_height()))
      pygame.draw.rect(child_surface, (255,0,0), child.rect, width=4)
      self.surface.blit(child_surface, child_rect)
      self.parent_surface.blit(self.surface,(self.margin_left,self.margin_top))
    if isinstance(child,pygame.Surface):
      self.surface.blit(child, child_rect)
      self.parent_surface.blit(self.surface,(self.margin_left,self.margin_top))

  @property
  def _grouped_positioning_children(self):
     grouped_children = []
     for child in self.children:
        if isinstance(child.content,pygame.Surface):
           grouped_children.append(child.content)
        elif isinstance(child.content,Container):
            if child.content.positioning == 'GROUPED':
              grouped_children.append(child.content)
     return grouped_children
  
  @property
  def _grouped_positioning_elements(self):
    grouped_children = []
    for child in self.children:
      if isinstance(child.content,pygame.Surface):
          grouped_children.append(child)
      elif isinstance(child.content,Container):
          if child.content.positioning == 'GROUPED':
            grouped_children.append(child)
    return grouped_children
  
  @property
  def _absolute_positioning_children(self):
    absolute_children = []
    for child in self.children:
      if isinstance(child.content,Container):
          absolute_children.append(child.content)
    return absolute_children
  
  @property
  def _absolute_positioning_elements(self):
    absolute_children = []
    for child in self.children:
      if isinstance(child.content,Container):
          absolute_children.append(child)
    return absolute_children
  
  def _render_grouped(self):

      def get_vertical_offset(child_index):
        '''
        Get vertical offset from center for a specific element
        '''
        vertical_offset = 0
        upper_index_limit = child_index
        for index,child in enumerate(self._grouped_positioning_elements):
            if index < upper_index_limit:
                vertical_offset += self._get_child_height(child.content)
            
            '''
            TODO: Update the element with the vertical offset
            '''
            if index == upper_index_limit:
                child.vertical_offset = vertical_offset
                return vertical_offset
              
            if index > upper_index_limit:
                child.vertical_offset = vertical_offset
                return vertical_offset
      
      def get_horizontal_offset(child_index):
          '''
          Get horizontal offset from center for given child element
          '''
          child = self._grouped_positioning_children[child_index]
          return self.get_width()//2 - self._get_child_centerx(child)
          # return get_total_width()*1.0/2
            
      def get_center_movement():
        # get the movement required for center
        screen_center_y = self.surface.get_rect().centery
        screen_center_x = self.surface.get_rect().centerx
        center_movement_x = screen_center_x - self.get_width()//2 # difference bettween horizontal center of screen and center of unioned children
        center_movement_y = screen_center_y - self.get_height()//2 # difference between vertical center of screen and center of unioned children
        return (center_movement_x,center_movement_y)


      # set the position of the elements
      for index, child in enumerate(self._grouped_positioning_children):
        # get the position of each element and compare against center
        vertical_offset = get_vertical_offset(index)
        horizontal_offset = get_horizontal_offset(index)
        center_movement_x,center_movement_y = get_center_movement()
        child_rect = child.get_rect()
        child_rect.move_ip(horizontal_offset + center_movement_x, vertical_offset + center_movement_y)
        self._blit_child_parent_surface(child,child_rect)
        

  def _render_absolute(self):
     for child in self._absolute_positioning_children:
        pass
     
  '''
  TODO: Modify to include optional ID argument
  '''
  def add_child(self,child, id=None):
    # surface.parent = self
    child = copy.copy(child)
    child_element = Container.Element(child,id=id, parent=self.element)
    self.children.append(child_element)
    
  def get_width(self):
      '''
      Get the total width of this container

      If layout is vertical, then knowing the total width can be inferred
      based on the maximum width rectangle
      '''
      if len(self._grouped_positioning_children) > 0:
        max_width = 0
        for child in self._grouped_positioning_children:
          if self._get_child_width(child) > max_width:
            max_width = self._get_child_width(child)
        return max_width
      elif len(self._grouped_positioning_children) == 0:
         return self.min_width
     
  
  def get_height(self):
    '''
    Get the total height of this container
    '''
    if len(self._grouped_positioning_children) > 0:
      total_height = 0
      for child in self._grouped_positioning_children:
        total_height += self._get_child_height(child)
      return total_height
    elif len(self._grouped_positioning_children) == 0:
      return self.min_height
  
  def get_rect(self):
     '''
     Get the PyGame rect object for this Container instance
     '''
     return pygame.Rect(0,0,self.min_width,self.min_height)
  
  def get_child(self, id):
     '''
     return the first element that matches the ID provided
     '''
     for element in self.children:
        if element.id == id:
           return element
  

  def render(self):
    '''
    This method sets the position of all the children elements of this container object. 
    The 'union' of the child surfaces is what effectively gets positioned.
    '''

    '''
    TODO: Create additional rendering logic for ABSOLUTE positioning of elements
    '''      
    self._render_grouped()
    self._render_absolute()

    self.surface.fill(self.fill_color)
    pygame.draw.rect(self.surface, (255,0,0), self.rect, width=4)
    self.parent_surface.blit(self.surface,(self.margin_left,self.margin_top))

