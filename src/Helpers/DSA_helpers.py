from collections import deque 

class Graph(object):
    def __init__(self):
        self.adjacency_list = {}
        self.vertex_dict = {}
        self.vertex_list = []
        self.numVertices = 0
        self.numEdges = 0
        self.edge_dict = {}

    def add_edge(self,v1,v2,w=None):
        if v1 not in self.vertex_dict:
            self.vertex_dict[v1] = None
            self.vertex_list.append(v1)
            self.adjacency_list[v1] = []
            self.edge_dict[v1] = {}
            self.numVertices+=1

        if v2 not in self.vertex_dict:
            self.vertex_dict[v2] = None
            self.vertex_list.append(v2)
            self.adjacency_list[v2] = []
            self.edge_dict[v2] = {}
            self.numVertices+=1

        if v2 not in self.edge_dict[v1]:
            self.adjacency_list[v1].append(v2)
            self.adjacency_list[v2].append(v1)
            self.edge_dict[v1][v2] = w
            self.edge_dict[v2][v1] = w
            self.numEdges += 1

    def compute_dist_dijkstra(self,start_vert,target_vert,return_path=False):
        if start_vert not in self.vertex_dict or target_vert not in self.vertex_dict:
            if return_path:
                return None,None
            else:
                return None

        myHeap = AugmentedHeap()
        myHeap.insert_item(0,start_vert)

        dist_dict = {}
        marked_dict = {}
        predecessor_dict = {start_vert:None}

        while not myHeap.isempty():
            current_dist, current_vert =myHeap.pop()

            if current_vert==target_vert:
                if return_path:
                    path_stack = [target_vert]
                    while predecessor_dict[path_stack[-1]] is not None:
                        path_stack.append(predecessor_dict[path_stack[-1]])

                    path_out = []
                    while len(path_stack)>0:
                        path_out.append(path_stack.pop(-1))

                    return current_dist,path_out
                else:
                    return current_dist
                
            dist_dict[current_vert]=current_dist

            for neighbor_vert in self.adjacency_list[current_vert]:
                if neighbor_vert not in dist_dict:

                    edge_weight = self.edge_dict[current_vert][neighbor_vert]

                    if edge_weight is None:
                        edge_weight = 1

                    neighbor_dist = current_dist+edge_weight

                    if neighbor_vert not in marked_dict:
                        myHeap.insert_item(neighbor_dist,neighbor_vert)
                        marked_dict[neighbor_vert]=True
                        predecessor_dict[neighbor_vert]=current_vert

                    elif neighbor_dist<myHeap.index_dict[neighbor_vert]:
                        myHeap.decrement_key(neighbor_dist,neighbor_vert)
                        predecessor_dict[neighbor_vert]=current_vert

        if return_path:
            return None,None
        else:
            return None

    def compute_dist_BFS(self,start_vert,target_vert,return_path=False):
        if start_vert not in self.vertex_dict or target_vert not in self.vertex_dict:
            if return_path:
                return None,None
            else:
                return None

        dist_dict = {start_vert:0}
        predecessor_dict = {start_vert:None}
        
        to_visit = deque()
        to_visit.append(start_vert)

        while len(to_visit)!=0:
            current_vert = to_visit.popleft()
            current_dist = dist_dict[current_vert]

            if current_vert == target_vert:
                if return_path:
                    path_stack = [target_vert]
                    while predecessor_dict[path_stack[-1]] is not None:
                        path_stack.append(predecessor_dict[path_stack[-1]])

                    path_out = []
                    while len(path_stack)>0:
                        path_out.append(path_stack.pop(-1))

                    return current_dist,path_out
                else:
                    return current_dist

            next_dist = current_dist+1
            for neighbor_vert in self.adjacency_list[current_vert]:
                if neighbor_vert not in dist_dict:
                    dist_dict[neighbor_vert] = next_dist
                    to_visit.append(neighbor_vert)
                    predecessor_dict[neighbor_vert]=current_vert

        if return_path:
            return None,None
        else:
            return None


    #adjacency_criteria(grid_in,(i0,j0),(i1,j1)) returns True or False
    #weight_func(grid_in,(i0,j0),(i1,j1)) returns edge weights
    def build_graph_from_2D_grid(self,grid_in,adjacency_criteria=None,weight_func=None,diags_allowed=False,horz_wrap=False,vert_wrap=False, dir_array=None):
        l0 = len(grid_in)
        if l0==0:
            return

        l1 = len(grid_in[0])
        if l1==0:
            return

        if dir_array is None:
            dir_array = [[1,0],[-1,0],[0,1],[0,-1]]

            if diags_allowed:
                dir_array += [[1,1],[-1,-1],[1,-1],[-1,1]]

        for i in range(l0):
            for j in range(l1):

                current_vert = (i,j)

                for direction in dir_array:
                    i_temp = i+direction[0]
                    j_temp = j+direction[1]

                    if vert_wrap:
                        i_temp%=l0

                    if horz_wrap:
                        j_temp%=l1

                    neighbor_vert = (i_temp,j_temp)

                    if 0<=i_temp and i_temp<l0 and 0<=j_temp and j_temp<l1:
                        add_edge_bool = True

                        if adjacency_criteria is not None:
                            add_edge_bool = adjacency_criteria(grid_in,current_vert,neighbor_vert)

                        if add_edge_bool:
                            edge_weight = None

                            if weight_func is not None:
                                edge_weight = weight_func(grid_in,current_vert,neighbor_vert)

                            self.add_edge(current_vert,neighbor_vert,edge_weight)

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

    def set_vertex_val(self,vertex,val=None):
        if vertex not in self.vertex_dict:
            self.vertex_list.append(vertex)
            self.forward_adjacency[vertex] = []
            self.reverse_adjacency[vertex] = []
            self.edge_dict[vertex] = {}
            self.numVertices+=1
            
        self.vertex_dict[vertex]=val

    def get_vertex_val(self,vertex):
        return self.vertex_dict[vertex]

    def contains_vertex(self,vertex):
        return vertex in self.vertex_dict

    #kosaraju's algorithm
    def build_metagraph(self):
        self.meta_forward_dict = []
        self.meta_reverse_dict = []
        
        self.meta_forward_list = []
        self.meta_reverse_list = []
        
        self.visited_dict = {}
        self.assigned_dict = {}
        self.assigned_lookup = {}
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
        if not self.visited_dict[u]:
            self.visited_dict[u]=True
            
            for v in self.forward_adjacency[u]:
                self.visit_kosaj(v)
            self.L.append(u)

    def assign(self, u, root):
        if self.assigned_dict[u]==-1:
            self.assigned_dict[u]=root
            if root not in self.assigned_lookup:
                self.assigned_lookup[root]=[]
            self.assigned_lookup[root].append(u)

            self.component_size_list[root]+=1
            for v in self.reverse_adjacency[u]:
                self.assign(v,root)
                
                prev_component = self.assigned_dict[v] 
                if prev_component!=root and prev_component not in self.meta_reverse_dict[root]:
                    self.meta_reverse_dict[root][prev_component]=None
                    self.meta_reverse_list[root].append(prev_component)
                    
                    self.meta_forward_dict[prev_component][root]=None
                    self.meta_forward_list[prev_component].append(root)

    def compute_dist_dijkstra(self,start_vert,target_vert,return_path=False):
        if start_vert not in self.vertex_dict or target_vert not in self.vertex_dict:
            if return_path:
                return None,None
            else:
                return None

        myHeap = AugmentedHeap()
        myHeap.insert_item(0,start_vert)

        dist_dict = {}
        marked_dict = {}
        predecessor_dict = {start_vert:None}

        while not myHeap.isempty():
            current_dist, current_vert =myHeap.pop()

            if current_vert==target_vert:
                if return_path:
                    path_stack = [target_vert]
                    while predecessor_dict[path_stack[-1]] is not None:
                        path_stack.append(predecessor_dict[path_stack[-1]])

                    path_out = []
                    while len(path_stack)>0:
                        path_out.append(path_stack.pop(-1))

                    return current_dist,path_out
                else:
                    return current_dist
                
            dist_dict[current_vert]=current_dist

            for neighbor_vert in self.forward_adjacency[current_vert]:
                if neighbor_vert not in dist_dict:

                    edge_weight = self.edge_dict[current_vert][neighbor_vert]

                    if edge_weight is None:
                        edge_weight = 1

                    neighbor_dist = current_dist+edge_weight

                    if neighbor_vert not in marked_dict:
                        myHeap.insert_item(neighbor_dist,neighbor_vert)
                        marked_dict[neighbor_vert]=True
                        predecessor_dict[neighbor_vert]=current_vert

                    elif neighbor_dist<myHeap.index_dict[neighbor_vert]:
                        myHeap.decrement_key(neighbor_dist,neighbor_vert)
                        predecessor_dict[neighbor_vert]=current_vert

        if return_path:
            return None,None
        else:
            return None

    def compute_dist_BFS(self,start_vert,target_vert,return_path=False):
        if start_vert not in self.vertex_dict or target_vert not in self.vertex_dict:
            if return_path:
                return None,None
            else:
                return None

        dist_dict = {start_vert:0}
        predecessor_dict = {start_vert:None}
        
        to_visit = deque()
        to_visit.append(start_vert)

        while len(to_visit)!=0:
            current_vert = to_visit.popleft()
            current_dist = dist_dict[current_vert]

            if current_vert == target_vert:
                if return_path:
                    path_stack = [target_vert]
                    while predecessor_dict[path_stack[-1]] is not None:
                        path_stack.append(predecessor_dict[path_stack[-1]])

                    path_out = []
                    while len(path_stack)>0:
                        path_out.append(path_stack.pop(-1))

                    return current_dist,path_out
                else:
                    return current_dist

            next_dist = current_dist+1
            for neighbor_vert in self.forward_adjacency[current_vert]:
                if neighbor_vert not in dist_dict:
                    dist_dict[neighbor_vert] = next_dist
                    to_visit.append(neighbor_vert)
                    predecessor_dict[neighbor_vert]=current_vert

        if return_path:
            return None,None
        else:
            return None

    #adjacency_criteria(grid_in,(i0,j0),(i1,j1)) returns True or False
    #weight_func(grid_in,(i0,j0),(i1,j1)) returns edge weights
    def build_graph_from_2D_grid(self,grid_in,adjacency_criteria=None,weight_func=None,diags_allowed=False,horz_wrap=False,vert_wrap=False, dir_array=None):
        l0 = len(grid_in)
        if l0==0:
            return

        l1 = len(grid_in[0])
        if l1==0:
            return

        if dir_array is None:
            dir_array = [[1,0],[-1,0],[0,1],[0,-1]]

            if diags_allowed:
                dir_array += [[1,1],[-1,-1],[1,-1],[-1,1]]

        for i in range(l0):
            for j in range(l1):

                current_vert = (i,j)

                for direction in dir_array:
                    i_temp = i+direction[0]
                    j_temp = j+direction[1]

                    if vert_wrap:
                        i_temp%=l0

                    if horz_wrap:
                        j_temp%=l1

                    neighbor_vert = (i_temp,j_temp)

                    if 0<=i_temp and i_temp<l0 and 0<=j_temp and j_temp<l1:
                        add_edge_bool = True

                        if adjacency_criteria is not None:
                            add_edge_bool = adjacency_criteria(grid_in,current_vert,neighbor_vert)

                        if add_edge_bool:
                            edge_weight = None

                            if weight_func is not None:
                                edge_weight = weight_func(grid_in,current_vert,neighbor_vert)

                            self.add_edge(current_vert,neighbor_vert,edge_weight)

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

class frequency_table(object):
    def __init__(self,list_in=None):
        self.freq_table = {}

        if list_in is not None:
            self.build_from_list(list_in)

    def build_from_list(self,list_in):
        for item in list_in:
            self.add_item(item)

    def add_item(self,item):
        if item in self.freq_table:
            self.freq_table[item]+=1
        else:
            self.freq_table[item]=1

    def remove_item(self,item,allow_negative=False):
        if item in self.freq_table:
            if self.freq_table[item]>0 or allow_negative:
                self.freq_table[item]-=1
        elif allow_negative:
            self.freq_table[item]=-1

    def __getitem__(self, item):
        if item in self.freq_table:
            return self.freq_table[item]
        else:
            return 0

    def __setitem__(self, item, freq):
        self.freq_table[item] = freq

    def __contains__(self, item):
        return (item in self.freq_table)

    def keys(self):
        return self.freq_table.keys()

    def __eq__(self, other):
        for key in self.keys():
            if key in other:
                if self[key]!=other[key]:
                    return False 
            else:
                if self[key]!=0:
                    return False
        for key in other.keys():
            if key in self:
                if self[key]!=other[key]:
                    return False
            else:
                if other[key]!=0:
                    return False

        return True

    def __str__(self):
        return self.freq_table.__str__()

    def max_frequency(self):
        max_val = 0

        for item in self.keys():
            max_val = max(max_val,self[item])

        return max_val