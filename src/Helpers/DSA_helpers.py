class Graph(object):
    def __init__(self):
        pass

class Digraph(object):
    def __init__(self):
        
        self.forward_adjacency = {}
        self.reverse_adjacency = {}
        self.adjacency_dict = {}
        self.vertex_dict = {}
        self.vertex_list = []
        self.numVertices = 0
        self.numEdges = 0
        self.edge_dict = {}

    def add_edge(self,v1,v2,w=None):
        if v1 not in self.vertex_dict:
            self.vertex_dict[v1] = None
            self.vertex_list.append(v1)
            self.forward_adjacency[v1] = []
            self.reverse_adjacency[v1] = []
            self.edge_dict[v1] = {}
            self.numVertices+=1

        if v2 not in self.vertex_dict:
            self.vertex_dict[v2] = None
            self.vertex_list.append(v2)
            self.forward_adjacency[v2] = []
            self.reverse_adjacency[v2] = []
            self.edge_dict[v2] = {}
            self.numVertices+=1

        if v2 not in self.edge_dict[v1]:
            self.forward_adjacency[v1].append(v2)
            self.edge_dict[v1][v2] = w
            self.reverse_adjacency[v2].append(v1)
            self.numEdges += 1

    def list_descendents(self,vertex):
        descendents_list = []
        self.visited_dict = {}

        self.list_descendents_recursive(vertex,descendents_list)

        return descendents_list

    def list_descendents_recursive(self,vertex,descendents_list):
        if vertex not in self.visited_dict:
            self.visited_dict[vertex]=None
            descendents_list.append(vertex)

            for child in self.forward_adjacency[vertex]:
                self.list_descendents_recursive(child,descendents_list)

    def list_ancestors(self,vertex):
        ancestors_list = []
        self.visited_dict = {}

        self.list_ancestors_recursive(vertex,ancestors_list)

        return ancestors_list

    def list_ancestors_recursive(self,vertex,ancestors_list):
        if vertex not in self.visited_dict:
            self.visited_dict[vertex]=None
            ancestors_list.append(vertex)

            for parent in self.reverse_adjacency[vertex]:
                self.list_ancestors_recursive(parent,ancestors_list)


    #kosaraju's algorithm
    def build_metagraph(self):
        self.meta_forward_dict = []
        self.meta_reverse_dict = []
        
        self.meta_forward_list = []
        self.meta_reverse_list = []
        
        self.visited_dict = {}
        self.assigned_dict = {}
        for vertex in self.vertex_list:
            self.visited_dict[vertex]=False
            self.assigned_dict[vertex]=-1
        self.L = []
        
        for vertex in self.vertex_list:
            self.visit_kosaj(vertex)
        
        
        self.component_size_list = []       
        count = 0
        while len(self.L)>0:
            u = self.L.pop(-1)
            
            if self.assigned_dict[u]==-1:
                self.component_size_list.append(0)
                
                self.meta_forward_dict.append({})
                self.meta_reverse_dict.append({})
                self.meta_forward_list.append([])
                self.meta_reverse_list.append([])
            
                self.assign(u,count)
                count+=1
        self.num_components = count
        
    def visit_kosaj(self,u):
        if not self.visited_list[u]:
            self.visited_list[u]=True
            
            for v in self.forward_adjacency[u]:
                self.visit_kosaj(v)
            self.L.append(u)

    def assign(self, u, root):
        if self.assigned_dict[u]==-1:
            self.assigned_dict[u]=root
            self.component_size_list[root]+=1
            for v in self.reverse_adjacency[u]:
                self.assign(v,root)
                
                prev_component = self.assigned_dict[v] 
                if prev_component!=root and prev_component not in self.meta_reverse_dict[root]:
                    self.meta_reverse_dict[root][prev_component]=None
                    self.meta_reverse_list[root].append(prev_component)
                    
                    self.meta_forward_dict[prev_component][root]=None
                    self.meta_forward_list[prev_component].append(root)

#a min heap by default
#can change to a max heap if desired
class AugmentedHeap(object):
    def __init__(self,useIndex_dict=True,isMaxHeap = False):
        self.isMinHeap = not isMaxHeap
        self.key_list = []
        self.val_list = []
        self.useIndex_dict = useIndex_dict
        if self.useIndex_dict:
            self.index_dict = {}

    def key_less_than(self,a,b):
        return (self.isMinHeap and a<b) or (not self.isMinHeap and a>b)

    def key_greater_than(self,a,b):
        return (self.isMinHeap and a>b) or (not self.isMinHeap and a<b) 

    def insert_item(self,key,val):
        self.key_list.append(key)
        self.val_list.append(val)
        if self.useIndex_dict:
            self.index_dict[val]=len(self.key_list)-1
        current_index = len(self.key_list)-1
        self.heapify_up(current_index)
            
    def isempty(self):
        if len(self.key_list)==0:
            return True
        else:
            return False
        
    def pop(self):
        if len(self.key_list)==0:
            return None, None
        
        mykey = self.key_list[0] 
        myval = self.val_list[0]
        if self.useIndex_dict:
            self.index_dict.pop(myval)
        
        if len(self.key_list)==1:
            self.key_list = []
            self.val_list = []
            return mykey,myval
        else:
            self.key_list[0] = self.key_list.pop(-1)
            self.val_list[0] = self.val_list.pop(-1)
            if self.useIndex_dict:
                self.index_dict[self.val_list[0]]=0
            
        current_index = 0
        self.heapify_down(current_index)
            
        return mykey,myval
    
    def delete_by_value(self,val):
        if len(self.key_list)!=0:
            self.decrement_key(self.key_list[0]-1,val)
            self.pop()
        
    def peak(self):
        if len(self.key_list)==0:
            return None, None
        
        return self.key_list[0], self.val_list[0]
    
    def peak_key(self):
        if len(self.key_list)==0:
            return None
        return self.key_list[0]
    
    def peak_val(self):
        if len(self.val_list)==0:
            return None
        return self.val_list[0]
    
    #only updates key if next key is closer to top of heap than old key
    def decrement_key(self,key,val):
        if self.useIndex_dict:
            current_index = self.index_dict[val]
            old_key = self.key_list[current_index]
            if self.key_less_than(key,old_key):
                self.key_list[current_index]=key
                self.heapify_up(current_index)
            
    def update_key(self,key,val):
        if self.useIndex_dict:
            current_index = self.index_dict[val]
            old_key = self.key_list[current_index]
            self.key_list[current_index]=key

            if self.key_less_than(key,old_key):
                self.heapify_up(current_index)

            elif self.key_greater_than(key,old_key):
                self.heapify_down(current_index)
            
    def heapify_up(self,current_index):
        next_index = (current_index-1)//2
        while current_index>0 and self.key_less_than(self.key_list[current_index],self.key_list[next_index]):
            temp = self.key_list[current_index]
            self.key_list[current_index] = self.key_list[next_index]
            self.key_list[next_index] = temp

            temp = self.val_list[current_index]
            self.val_list[current_index] = self.val_list[next_index]
            self.val_list[next_index] = temp
            
            if self.useIndex_dict:
                self.index_dict[self.val_list[current_index]]=current_index
                self.index_dict[self.val_list[next_index]]=next_index

            current_index = next_index
            next_index = (next_index-1)//2

    def heapify_down(self,current_index):
        max_index = len(self.key_list)
        while current_index*2+1 < max_index:
            index_left = current_index*2+1
            index_right = current_index*2+2
            switch_index = None
            if index_right < max_index:
                if (self.key_less_than(self.key_list[current_index], self.key_list[index_left]) and 
                    self.key_less_than(self.key_list[current_index], self.key_list[index_right])):
                    break
                else:
                    if  self.key_less_than(self.key_list[index_left],self.key_list[index_right]):
                        switch_index = index_left
                    else:
                         switch_index = index_right   
            else:
                if self.key_less_than(self.key_list[current_index], self.key_list[index_left]):
                    break
                else: 
                    switch_index = index_left

            temp = self.key_list[switch_index]
            self.key_list[switch_index] = self.key_list[current_index]
            self.key_list[current_index] = temp

            temp = self.val_list[switch_index]
            self.val_list[switch_index] = self.val_list[current_index]
            self.val_list[current_index] = temp

            if self.useIndex_dict:
                self.index_dict[self.val_list[current_index]]=current_index
                self.index_dict[self.val_list[switch_index]]=switch_index

            current_index = switch_index