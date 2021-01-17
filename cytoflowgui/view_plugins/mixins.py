'''
Created on Jan 16, 2021

@author: brian
'''

import os

from traits.api import HasTraits, on_trait_change, Property, HTML
from traitsui.api import View, Item, HGroup, TextEditor, InstanceEditor

import cytoflow.utility as util
from cytoflowgui.editors import TabListEditor

class PluginHelpMixin(HasTraits):
    """
    A mixin to get online HTML help for a class.  It determines the HTML
    path name from the class name.
    """
    
    _cached_help = HTML
    
    def get_help(self):
        """
        Gets the HTML help for this class.
        
        Returns
        -------
        string
            The HTML help in a single string.
        """
        
        if self._cached_help == "":
            current_dir = os.path.abspath(__file__)
            help_dir = os.path.split(current_dir)[0]
            help_dir = os.path.split(help_dir)[0]
            help_dir = os.path.join(help_dir, "help")
             
            view = self.get_view()
            help_file = None
            for klass in view.__class__.__mro__:
                mod = klass.__module__
                mod_html = mod + ".html"
                 
                h = os.path.join(help_dir, mod_html)
                if os.path.exists(h):
                    help_file = h
                    break
                 
            with open(help_file, encoding = 'utf-8') as f:
                self._cached_help = f.read()
                 
        return self._cached_help
    
        
                        
# class PluginViewMixin(HasTraits):
#     handler = Instance(Handler, transient = True)    
#     
#     # transmit some change back to the workflow
#     changed = Event
    

class ViewHandlerMixin(HasTraits):
    """
    Useful bits for view handlers.
    """
    
    # the view for the current plot
    current_plot_view = \
        View(
            HGroup(
                Item('plot_names_by',
                     editor = TextEditor(),
                     style = "readonly",
                     show_label = False),
                Item('current_plot',
                     editor = TabListEditor(name = 'plot_names'),
                     style = 'custom',
                     show_label = False)))
        
#     plot_params_traits = View(Item('plot_params',
#                                    editor = InstanceEditor(),
#                                    style = 'custom',
#                                    show_label = False))
    
    #context = Instance(WorkflowItem)
    
    conditions_names = Property(depends_on = "context.conditions")
    previous_conditions_names = Property(depends_on = "context.previous_wi.conditions")
    statistics_names = Property(depends_on = "context.statistics")
    numeric_statistics_names = Property(depends_on = "context.statistics")
    
    # MAGIC: gets value for property "conditions_names"
    def _get_conditions_names(self):
        if self.context and self.context.conditions:
            return sorted(list(self.context.conditions.keys()))
        else:
            return []
    
    # MAGIC: gets value for property "previous_conditions_names"
    def _get_previous_conditions_names(self):
        if self.context and self.context.previous_wi and self.context.previous_wi.conditions:
            return sorted(list(self.context.previous_wi.conditions.keys()))
        else:
            return []
        
    # MAGIC: gets value for property "statistics_names"
    def _get_statistics_names(self):
        if self.context and self.context.statistics:
            return sorted(list(self.context.statistics.keys()))
        else:
            return []

    # MAGIC: gets value for property "numeric_statistics_names"
    def _get_numeric_statistics_names(self):
        if self.context and self.context.statistics:
            return sorted([x for x in list(self.context.statistics.keys())
                                 if util.is_numeric(self.context.statistics[x])])
        else:
            return []

    @on_trait_change('context.view_error_trait', 
                     dispatch = 'ui', 
                     post_init = True)
    def _view_trait_error(self):
        
        # check if we're getting called on the local or remote process
        if self.info is None or self.info.ui is None:
            return
        
        for ed in self.info.ui._editors:  
                          
            if ed.name == self.context.view_error_trait:
                err_state = True
            else:
                err_state = False

            if not ed.label_control:
                continue
            
            item = ed.label_control
            
            if not err_state and not hasattr(item, '_ok_color'):
                continue
            
            pal = QtGui.QPalette(item.palette())  # @UndefinedVariable
            
            if err_state:
                setattr(item, 
                        '_ok_color', 
                        QtGui.QColor(pal.color(item.backgroundRole())))  # @UndefinedVariable
                pal.setColor(item.backgroundRole(), QtGui.QColor(255, 145, 145))  # @UndefinedVariable
                item.setAutoFillBackground(True)
                item.setPalette(pal)
            else:
                pal.setColor(item.backgroundRole(), item._ok_color)
                delattr(item, '_ok_color')
                item.setAutoFillBackground(False)
                item.setPalette(pal)
  