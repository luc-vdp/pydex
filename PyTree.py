 # -*- coding: utf-8 -*-
"""
pydex - Python Data Exploration Tool - Tree

@date: 2017-12-08

@author: luc.vandeputte@arcelormittal.com
"""

#%% Import libraries
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tkinter import simpledialog
import getpass
import datetime
import database


#%% Class definition
class PyTree(ttk.Frame):
    def __init__(self, master = None, connectionString = None, table = None, filterColumn = None, filterId = None, id = None):        
        # Define connectionsString and table
        if connectionString is None:
            self.connectionString = "DRIVER={SQL Server Native Client 11.0};Server=PA-LPUTTE;Database=Metadata;Trusted_Connection=yes;"
            self.table = 'Connections'
        else:
            self.connectionString = connectionString
            self.table = table
        
        # Copy filterColumn and filterId
        self.filterColumn = filterColumn
        self.filterId = filterId    
    
        # Construct the Frame object.
        ttk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
    
        # Create the popup menu
        self.createPopupMenu()
    
        # Create the widgets
        self.createWidgets()
    
        # Define events
        self.treeview.bind('<<TreeviewSelect>>', self.selectItem)
        self.treeview.bind('<Double-Button-1>', self.executeItem)
        self.treeview.bind("<Button-3>", self.popupMenu)
        
        # Initialize variable
        self.moveId = ''   
    
        #Select the connection if specified
        if id != None:
            try:
                # Make sure that item is visible
                self.treeview.see(id)
                # Select item in tree            
                self.treeview.selection_set(id)
                # Set focus on the item
                self.treeview.focus(id)
            except:
                pass
            
    def FullTitle(self):
        # Get selected tree item
        id = self.treeview.focus()
        text = self.treeview.item(id)['text']
        id = self.treeview.parent(id)
        while id != '':
            text = self.treeview.item(id)['text'] + ' - ' + text
            id = self.treeview.parent(id)
        return text
    
    # Actions to do when a treeview item is right clicked
    def popupMenu(self, event):
        # Display the popup menu
        try:
            #self.popup.selection = self.treeview.set(self.treeview.identify_row(event.y))
            self.popup.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup.grab_release()
   
    # Actions to do when a treeview item is selected
    def selectItem(self, event):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Propagate the event
        self.master.event_generate('<<TreeviewSelect>>')

    # Actions to do when a treeview item is double clicked
    def executeItem(self, event):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Propagate the event
        self.master.event_generate('<<Double-Button-1>>')

    def editTreeItem(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Propagate the event
        self.master.event_generate('<<TreeviewEdit>>')

    def renameTreeItem(self):
        # Get Id of selected item
        self.Id = self.treeview.focus()
        # Get text of selected item
        oldText = self.treeview.item(self.Id)['text']        
        # Ask new text
        newText = simpledialog.askstring("Rename", "New name?", initialvalue=oldText, parent=self)
        # If new text given
        if newText == '':
            messagebox.showerror(title="Error", message="Text should not be empty")            
        elif newText != None:
            # Write update query
            query = ("Update " + self.table + 
                     " set [Title] = '" + newText + "' " + 
                     "   , [UserId] = '" + getpass.getuser() + "' " + 
                     "   , [TimeChanged] = '" + str(datetime.datetime.now()) + "' " + 
                     "Where Id = " + self.Id )
            if self.filterColumn != None:
                query += " And " + self.filterColumn + " = " + self.filterId
            # Execute update query
            database.setData(self.connectionString, query)
            # Refresh the tree and select the renamed item
            self.refreshTree(self.Id)
            
    def moveTreeItem(self):
        # if no items in tree yet
        if len(self.treeview.get_children('')) == 0:
            messagebox.showinfo(title="Error", message="Nothing to move")
        else:
            # Get Id of item to be moved
            self.moveId = self.treeview.focus()
            # If asked to move
            if self.popup.entrycget(3, 'label') == 'Move...':
                # Show info about how to proceed
                self.labelInfo.grid(row = 0, column = 0, sticky = tk.E, padx =2, pady=2)
                # Change menu item to 'Cancel move...'
                self.popup.entryconfig(3, label='Cancel move')
            else:
                # Cancel move
                self.moveFinished()
        
    def addTreeItemBefore(self):
        # If there is an item to be moved...
        if self.moveId != '':
            # Move item before selected node
            self.moveItemBeforeNode()
        elif len(self.treeview.get_children('')) == 0:
            # Add first item in the tree
            self.addItemInNode()
        else:
            # Add new item before the selected node
            self.addItemBeforeNode()
        # Allow to edit the details
        self.master.event_generate('<<TreeviewEdit>>')

    def addTreeItemAfter(self):
        # If there is an item to be moved...
        if self.moveId != '':
            # Move item after selected node
            self.moveItemAfterNode()
        elif len(self.treeview.get_children('')) == 0:
            # Add first item in the tree
            self.addItemInNode()
        else:            
            # Add new item after the selected node
            self.addItemAfterNode()
        # Allow to edit the details
        self.master.event_generate('<<TreeviewEdit>>')
                
    def addTreeItemIn(self):
        # If there is an item to be moved...
        if self.moveId != '':
            # Move item in selected node
            self.moveItemInNode()
        else:
            # Add new item in the selected node
            self.addItemInNode()
        # Allow to edit the details
        self.master.event_generate('<<TreeviewEdit>>')

    def moveAllowed(self):
        if self.Id == self.moveId:
            messagebox.showinfo(message="Cannot move node in or after itself")
        else:
            # Get selected node
            nodeId = self.Id
            # Check parents of selected node to see if the selected nod is in the node to be moved
            while (self.treeview.parent(nodeId) != '') & (nodeId != self.moveId):
                nodeId = self.treeview.parent(nodeId)
            # If one of the parents is the node to be moved...
            if nodeId == self.moveId:
                # Tell we do not allow that
                messagebox.showinfo(message="Can not move node in itself")
            else:
                # Move is allowed
                return True
    
    def addItemAfterNode(self):
        # Ask new text
        newText = simpledialog.askstring("Add after", "New name?", parent=self)
        # If filled in...
        if newText != None:
            # Get the selected id
            id = self.treeview.focus()
            # Get Parent Id
            parentId = self.treeview.parent(id)
            # For the top level the parent id is an empty string in tkinter, but 0 in the database
            if parentId == '':
                parentId = '0'
            # Get index (in the database we start at 1, while python starts at 0)
            nr = self.treeview.index(id) + 1
                    
            # Shift items After selected node
            query = ("Update " + self.table +
                     " Set Nr = Nr + 1 " +
                     "Where ParentId = " + parentId +
                     "  And Nr > " + str(nr) +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                query += "  And " + self.filterColumn + " = " + self.filterId         
            # Execute update query
            database.setData(self.connectionString, query)
            
            # Insert item after selected node
            if self.filterColumn != None:
                # Table contains an Id to store multiple trees in 1 table
                query = ("Insert Into " + self.table +
                         " (Status, ParentId, [Level], Nr, Title, UserId, " + self.filterColumn + ") " +
                         "Select Status, ParentId, [Level] , Nr + 1, '" + newText + "', '" + getpass.getuser() + "' ," + self.filterId + 
                         " From " + self.table +
                         " Where Id = " + id +
                         "  And " + self.filterColumn + " = " + self.filterId)
            else:
                # Table does not contain an Id to store multiple trees in 1 table
                query = ("Insert Into " + self.table +
                         " (Status, ParentId, [Level], Nr, Title, UserId) " +
                         "Select Status, ParentId, [Level] , Nr + 1, '" + newText + "', '" + getpass.getuser() + "' " +
                         " From " + self.table +
                         " Where Id = " + id)
            # Execute insert query
            database.setData(self.connectionString, query)
    
            # Select the new item
            self.refreshTree(id, 1)

    def addItemBeforeNode(self):
        # Ask new text
        newText = simpledialog.askstring("Add before", "New name?", parent=self)
        # If filled in...
        if newText != None:
            # Get the selected id
            id = self.treeview.focus()
            # Get Parent Id
            parentId = self.treeview.parent(id)
            # For the top level the parent id is an empty string in tkinter, but 0 in the database
            if parentId == '':
                parentId = '0'
            # Get index (in the database we start at 1, while python starts at 0)
            nr = self.treeview.index(id) + 1
                    
            # Shift slected node and next nodes
            query = ("Update " + self.table +
                     " Set Nr = Nr + 1 " +
                     "Where ParentId = " + parentId +
                     "  And Nr >= " + str(nr) +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                self.query += "  And " + self.filterColumn + " = " + self.filterId         
            # Execute update query
            database.setData(self.connectionString, query)
            
            # Insert item before selected node
            if self.filterColumn != None:
                # Table contains an Id to store multiple trees in 1 table
                query = ("Insert Into " + self.table +
                         " (Status, ParentId, [Level], Nr, Title, UserId, " + self.filterColumn + ") " +
                         "Select Status, ParentId, [Level] , Nr - 1 , '" + newText + "', '" + getpass.getuser() + "' ," + self.filterId + 
                         " From " + self.table +
                         " Where Id = " + id +
                         "  And " + self.filterColumn + " = " + self.filterId)
            else:
                # Table does not contain an Id to store multiple trees in 1 table
                query = ("Insert Into " + self.table +
                         " (Status, ParentId, [Level], Nr, Title, UserId) " +
                         "Select Status, ParentId, [Level] , Nr - 1, '" + newText + "', '" + getpass.getuser() + "' " +
                         " From " + self.table +
                         " Where Id = " + id)
            # Execute insert query
            database.setData(self.connectionString, query)
    
            # Select the new item
            self.refreshTree(id, -1)

    def moveItemAfterNode(self):
        # Check if the move is allowed
        if self.moveAllowed():
            # Get information (ParentId, Level, Nr) about selected (target) node 
            query = ("Select Id, ParentId, [Level], Nr " +
                     "From " + self.table + " " +
                     "Where Id = " + self.Id +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                query += "  And " + self.filterColumn + " = " + self.filterId
    
            data = database.getData(self.connectionString, query)
            
            if len(data.index) != 1:
                messagebox.showinfo(message="Move not succeeded")
            else:
                selParentId = str(data.ParentId[0])
                selLevel = str(data.Level[0])
                selNr = str(data.Nr[0])

                # Get information about node being moved
                query = ("Select Id, ParentId, [Level], Nr " +
                         "From " + self.table + " " +
                         "Where Id = " + self.moveId +
                         "  And Status = 'A' ")
                if self.filterColumn != None:
                    query += "  And " + self.filterColumn + " = " + self.filterId
        
                data = database.getData(self.connectionString, query)

                if len(data.index) != 1:
                    messagebox.showinfo(message="Move not succeeded")
                else:
                    moveParentId = str(data.ParentId[0])
                    moveLevel = str(data.Level[0])
                    moveNr = str(data.Nr[0])

                    # Shift items after selected (target) node down
                    query = ("Update " + self.table + " " +
                             "Set Nr = Nr + 1 " +
                             "Where ParentId = " + selParentId +
                             "  And Nr > " + selNr +
                             "  And Status = 'A' ")
                    if self.filterColumn != None:
                        query += "  And " + self.filterColumn + " = " + self.filterId
            
                    database.setData(self.connectionString, query)
                    
                    # Update moved node's ParentId, LevelNr and SeqNr
                    query = ("Update " + self.table + " Set " +
                             "ParentId = " + selParentId + ", " +
                             "[Level] = " + selLevel + ", " +
                             "Nr = " + selNr + " + 1 " +
                             "Where Id = " + self.moveId +
                             "  And Status = 'A' ")
                    if self.filterColumn != None:
                        query += "  And " + self.filterColumn + " = " + self.filterId
                    
                    database.setData(self.connectionString, query)
            
                    # Shift items (if any) after moved node up
                    query = ("Update " + self.table + " " +
                             "Set Nr = Nr - 1 " +
                             "Where ParentId = " + moveParentId +
                             "  And Nr > " + moveNr +
                             "  And Status = 'A' ")
                    if self.filterColumn != None:
                        query += "  And " + self.filterColumn + " = " + self.filterId
                    
                    database.setData(self.connectionString, query)
            
                    # Update level of children of moved node if necessary
                    if selLevel != moveLevel:
                        self.adaptLevelOfChildren(self.moveId, selLevel)

        # Refresh treeview
        self.refreshTree(self.moveId)

        # Indicate that there is nothing to move anymore
        self.moveFinished()

    def moveItemBeforeNode(self):
        # Check if the move is allowed
        if self.moveAllowed():
            # Get information (ParentId, Level, Nr) about selected (target) node 
            query = ("Select Id, ParentId, [Level], Nr " +
                     "From " + self.table + " " +
                     "Where Id = " + self.Id +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                query += "  And " + self.filterColumn + " = " + self.filterId
    
            data = database.getData(self.connectionString, query)
            
            if len(data.index) != 1:
                messagebox.showinfo(message="Move not succeeded")
            else:
                selParentId = str(data.ParentId[0])
                selLevel = str(data.Level[0])
                selNr = str(data.Nr[0])

                # Get information about node being moved
                query = ("Select Id, ParentId, [Level], Nr " +
                         "From " + self.table + " " +
                         "Where Id = " + self.moveId +
                         "  And Status = 'A' ")
                if self.filterColumn != None:
                    query += "  And " + self.filterColumn + " = " + self.filterId
        
                data = database.getData(self.connectionString, query)

                if len(data.index) != 1:
                    messagebox.showinfo(message="Move not succeeded")
                else:
                    moveParentId = str(data.ParentId[0])
                    moveLevel = str(data.Level[0])
                    moveNr = str(data.Nr[0])

                    # Shift items after selected (target) node down (including selected node itself)
                    query = ("Update " + self.table + " " +
                             "Set Nr = Nr + 1 " +
                             "Where ParentId = " + selParentId +
                             "  And Nr >= " + selNr +
                             "  And Status = 'A' ")
                    if self.filterColumn != None:
                        query += "  And " + self.filterColumn + " = " + self.filterId
            
                    database.setData(self.connectionString, query)

                    # Update moved node's ParentId, LevelNr and SeqNr
                    query = ("Update " + self.table + " Set " +
                             "ParentId = " + selParentId + ", " +
                             "[Level] = " + selLevel + ", " +
                             "Nr = " + selNr + " " +
                             "Where Id = " + self.moveId +
                             "  And Status = 'A' ")
                    if self.filterColumn != None:
                        query += "  And " + self.filterColumn + " = " + self.filterId

                    database.setData(self.connectionString, query)
            
                    # Shift items (if any) after moved node up
                    query = ("Update " + self.table + " " +
                             "Set Nr = Nr - 1 " +
                             "Where ParentId = " + moveParentId +
                             "  And Nr > " + moveNr +
                             "  And Status = 'A' ")
                    if self.filterColumn != None:
                        query += "  And " + self.filterColumn + " = " + self.filterId
                    
                    database.setData(self.connectionString, query)
            
                    # Update level of children of moved node if necessary
                    if selLevel != moveLevel:
                        self.adaptLevelOfChildren(self.moveId, selLevel)

        # Refresh treeview
        self.refreshTree(self.moveId)

        # Indicate that there is nothing to move anymore
        self.moveFinished()

    def moveItemInNode(self):
        # Get information about selectd parent node and it's children
        ParentId = self.Id
        
        query = ("Select A.ParentId, A.[Level], max(B.Nr) As NrOfChildren " +
                 "From " + self.table + " A " +
                 "Left outer join " + self.table + " B " +
                 "On A.Id = B.ParentId " +
                 "Where A.Id = " + ParentId + " " +
                 "  And A.Status = 'A' ")
        if self.filterColumn != None:
            query += "  And " + self.filterColumn + " = " + self.filterId
        query += " Group By A.ParentId, A.[Level]"

        data = database.getData(self.connectionString, query)

        if len(data.index) != 1:
            messagebox.showinfo(message="Move not succeeded")
        else:
            Level = str(data.Level[0] + 1)

            if data.NrOfChildren[0] != None:
                Nr = str(data.NrOfChildren[0] + 1)
            else:
                Nr = '1'

            #Get information about node being moved
            query = ("Select Id, ParentId, [Level], Nr " +
                     "From " + self.table + " " +
                     "Where Id = " + self.moveId +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                query += "  And " + self.filterColumn + " = " + self.filterId
            
            data = database.getData(self.connectionString, query)
    
            if len(data.index) != 1:
                messagebox.showinfo(message="Move not succeeded")
            else:
                ParentIdMoved = str(data.ParentId[0])
                LevelMoved = str(data.Level[0])
                NrMoved = str(data.Nr[0])

            #Insert under target node 
            query = ("Update " + self.table + " Set " +
                     "ParentId = " + ParentId + ", " +
                     "[Level] = " + Level + ", " +
                     "Nr = " + Nr + " " +
                     "Where Id = " + self.moveId +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                query += "  And " + self.filterColumn + " = " + self.filterId
            
            database.setData(self.connectionString, query)
    
            #Shift items (if any) after moved node up
            query = ("Update " + self.table + " " +
                     "Set Nr = Nr - 1 " +
                     "Where ParentId = " + ParentIdMoved +
                     "  And Nr > " + NrMoved +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                query += "  And " + self.filterColumn + " = " + self.filterId
            
            database.setData(self.connectionString, query)
    
            #Update level of children of moved node if necessary
            if Level != LevelMoved:
                self.adaptLevelOfChildren(self.moveId, Level)
        
        # Refresh treeview
        self.refreshTree(self.moveId)

        # Indicate that there is nothing to move anymore
        self.moveFinished()

       
    def moveFinished(self):
        # Indicate that there is nothing to move anymore
        self.moveId = ''
        # Hide info label
        self.labelInfo.grid_forget()
        # Change menu item back to 'Move...'
        self.popup.entryconfig(3, label='Move...')


    def addItemInNode(self):
        # if no items in tree yet...
        if len(self.treeview.get_children('')) == 0:
            # Ask new text
            newText = simpledialog.askstring("Add in", "New name?", parent=self)   
            # If text given...
            if newText != None:
                # Write insert query
                if self.filterId == None:
                    # Table does not contain an Id to store multiple trees in 1 table
                    query = ("Insert Into " + self.table + 
                            " (Status, ParentId, [Level], Nr, Title, UserId) " +
                            " values('A', 0, 1, 1, '" + newText + "', '" + getpass.getuser() +"') ")
                else:
                    # Table contains an Id to store multiple trees in 1 table
                    query = ("Insert Into " + self.table + 
                             " (Status, ParentId, [Level], Nr, Title, UserId, " + self.filterColumn + " ) " +
                             " values('A', 0, 1 , 1, '" + newText + "', '" + getpass.getuser() + "', " + self.filterId)

                # Execute insert query
                database.setData(self.connectionString, query)

                # Refresh the tree
                self.refreshTree()

        else:
            # Already items in tree -> get selected item
            id = self.treeview.focus()
            # If item already has children...
            if len(self.treeview.get_children(self.Id)) > 0:
                # Don't allow to use "Add in"
                messagebox.showinfo(message="This item already contains items. Use the 'Add after...' command")  
                newText = None
            else:
                # Ask new text
                newText = simpledialog.askstring("Add in", "New name?", parent=self)
                # If text given...
                if newText != None:
                    # Write insert query
                    if self.filterId == None:
                        # Table does not contain an Id to store multiple trees in 1 table
                        query = ("Insert Into " + self.table + 
                                " (Status, ParentId, [Level], Nr, Title, UserId) " +
                                "Select Status, Id, [Level] + 1, 1, '" + newText + "', '" + getpass.getuser() +"' " +
                                "From " + self.table + " " +
                                "Where Id = " + self.Id +
                                "  And Status = 'A' ")
                    else:
                        # Table contains an Id to store multiple trees in 1 table
                        query = ("Insert Into " + self.table + 
                                 " (Status, ParentId, [Level], Nr, Title, UserId, " + self.filterColumn + " ) " +
                                 "Select Status, Id, [Level] + 1, 1, '" + newText + "', '" + getpass.getuser() + "', " + self.filterId + " " +
                                 "From " + self.table + " " +
                                 "Where Id = " + self.Id +
                                 "  And Status = 'A' "
                                 "  And " + self.filterColumn + " = " + self.filterId)
        
                    # Execute insert query
                    database.setData(self.connectionString, query)

                    # Refresh the tree
                    self.refreshTree()
        
                    # Select the new child
                    for child in self.treeview.get_children(id):  
                        # Make sure that item is visible
                        self.treeview.see(child)
                        # Select item in tree            
                        self.treeview.selection_set(child)
                        # Set focus on the item
                        self.treeview.focus(child)

    def adaptLevelOfChildren(self, ParentId, ParentLevel):
        # Get children
        query = ("Select Id, ParentId, [Level], Nr " +
                 "From " + self.table + " " +
                 "Where ParentId = " + ParentId +
                 "  And Status = 'A' ")
        if self.filterColumn != None:
            query += "  And " + self.filterColumn + " = " + self.filterId

        tbl = database.getData(self.connectionString, query)

        for row in tbl.itertuples():
            Id = str(row.Id)
            # Update Level
            query = ("Update " + self.table + " Set " +
                     "[Level] = " + ParentLevel + " + 1 " +
                     "Where Id = " + Id +
                     "  And Status = 'A' ")
            if self.filterColumn != None:
                query += "  And " + self.filterColumn + " = " + self.filterId

            database.setData(self.connectionString, query)
            # Update level of children of this child
            self.adaptLevelOfChildren(Id, str(int(ParentLevel) + 1))

    def deleteTreeItem(self):
        # Get selected tree item
        self.Id = self.treeview.focus()
        # Print it
        print('deleteTreeItem ' + self.Id)

    # Refresh the tree (and optionally select the given id)
    def refreshTree(self, id=None, next=0):
        # Clear existing content in treeview
        self.treeview.delete(*self.treeview.get_children())

        # Write query to get tree data
        query = "Select * From " + self.table + " Where Status = 'A' " 
        if self.filterColumn != None:
            query += " And " + self.filterColumn + " = " + self.filterId
        query += " Order By [Level], Nr"
        
        # Execute query to and get the data
        treedata = database.getData(self.connectionString, query)
        
        # Fill tree
        for i in treedata.index:
            if (i==0) | (treedata.ParentId[i]==0):
                self.treeview.insert('', treedata.Nr[i]-1, iid=treedata.Id[i], text=treedata.Title[i].strip())
            else:
                self.treeview.insert(treedata.ParentId[i], treedata.Nr[i]-1, iid=treedata.Id[i], text=treedata.Title[i].strip())

        # If the tree has items    
        if treedata.Id.count() > 0:
            # Select the given id
            if id != None:
                # If we should show the next item
                if next == 1:
                    # Get the id of the next item
                    id = self.treeview.next(id)
                elif next == -1:
                    # Get the id of the previous item
                    id = self.treeview.prev(id)

                # Make sure that item is visible
                self.treeview.see(id)
                # Select item in tree            
                self.treeview.selection_set(id)
                # Set focus on the item
                self.treeview.focus(id)
            else:
                # Open first treeview item
                self.treeview.item(treedata.Id[0], open=True)
                
    def createPopupMenu(self):
        #Create menu
        self.popup = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Edit...", command=self.editTreeItem)
        self.popup.add_command(label="Rename...", command=self.renameTreeItem)
        self.popup.add_separator()
        self.mnuMove = tk.StringVar()
        self.popup.add_command(label="Move...", command=self.moveTreeItem)
        self.popup.add_command(label="Add before...", command=self.addTreeItemBefore)
        self.popup.add_command(label="Add after...", command=self.addTreeItemAfter)
        self.popup.add_command(label="Add in...", command=self.addTreeItemIn)
        self.popup.add_separator()
        self.popup.add_command(label="Delete...", command=self.deleteTreeItem)
        self.popup.add_separator()
        self.popup.add_command(label="Refresh", command=self.refreshTree)
        
    def createWidgets(self):
        # Get top window 
        self.top = self.winfo_toplevel()
        
        # Make it stretchable         
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        

        # Make rows and columns stretchable
        self.rowconfigure(1, weight=1)        
        self.columnconfigure(0, weight=1)        

        # Label
        self.labelInfo = ttk.Label(self, text="Select destination and choose right click to add..")
        self.labelInfo.grid(row = 0, column = 0, sticky = tk.E, padx =2, pady=2)
        self.labelInfo.grid_forget()
        
        # Tree
        self.treeview = ttk.Treeview(self)
        self.treeview.grid(row = 1, column = 0, rowspan=12, sticky = tk.NE + tk.SW, padx =2, pady=2)
        self.treeview['show'] = 'tree'
        self.treeview.column('#0', stretch=tk.YES, minwidth=500, width=200)          
        self.refreshTree()
        
        # Vertical scrollbar
        scrollVertical = ttk.Scrollbar(self)       
        scrollVertical.grid(row=1, column=1, sticky=tk.NE+tk.SW)
        scrollVertical.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollVertical.set)

        # Horizontal scrollbar
        scrollHorizontal = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollHorizontal.grid(row=2, column=0, sticky=tk.NE+tk.SW)
        scrollHorizontal.configure(command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=scrollHorizontal.set)


# Allow the class to run stand-alone.
if __name__ == "__main__":
    PyTree().mainloop()

