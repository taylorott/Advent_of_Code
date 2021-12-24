classdef OrionHashTable < handle
    properties
        m;
        my_key_table;
        my_value_table;
        inner_prod_vector;
    end
    
    methods
        function obj = OrionHashTable(m)
            obj.m=m;
            obj.my_key_table = {};
            obj.my_value_table = {};
            
            for i = 1:m
                obj.my_key_table{i}={};
                obj.my_value_table{i} ={};
            end
            obj.inner_prod_vector = [];
        end
        
        function hash_index = my_hash_function(obj,my_key)
            if length(obj.inner_prod_vector)==0
               obj.inner_prod_vector = randi(obj.m,[length(my_key),1]); 
            end
            hash_index = mod(sum(obj.inner_prod_vector'.*my_key),obj.m)+1;
        end
        
        function [hash_index,key_index] = get_key_index(obj,my_key)
            hash_index = obj.my_hash_function(my_key);
            key_index=1;
            while key_index<=length(obj.my_key_table{hash_index}) && prod(obj.my_key_table{hash_index}{key_index}==my_key)==0
                key_index=key_index+1;
            end
%             if key_index<=length(obj.my_key_table{hash_index})
%                 'found key'
%                 [obj.my_key_table{hash_index}{key_index};my_key]
%             end
        end
        
        function insert(obj,my_key,my_value)
            hash_index = obj.my_hash_function(my_key);
%             my_key
%             obj.my_key_table{hash_index}
%             size(obj.my_key_table{hash_index},1)
%             obj.my_key_table
%             'hello!'
%             obj.my_key_table{hash_index}
            if length(obj.my_key_table{hash_index})==0
                obj.my_key_table{hash_index} = {};
                obj.my_value_table{hash_index} = {};
            end
            obj.my_key_table{hash_index}{end+1} = my_key;
            obj.my_value_table{hash_index}{end+1} = my_value;
        end
        
        function update_value(obj,my_key,my_value)
            [hash_index,key_index] = obj.get_key_index(my_key);
            
            obj.my_value_table{hash_index}{key_index} = my_value;
            
        end
        
        function my_value = get_value(obj,my_key)
            [hash_index,key_index] = obj.get_key_index(my_key);
            my_value = obj.my_value_table{hash_index}{key_index};
        end
        
        function delete_key(obj,my_key)
            [hash_index,key_index] = obj.get_key_index(my_key);
            old_key_table = obj.my_key_table{hash_index};
            old_value_table = obj.my_value_table{hash_index};
                      
            obj.my_key_table{hash_index} =  {};            
            obj.my_value_table{hash_index} =  {};
            
            count=1;
            for i = 1:length(old_key_table)
                if i~=key_index
                    obj.my_key_table{hash_index}{count} = old_key_table{i};
                    obj.my_value_table{hash_index}{count} = old_value_table{i};
                    count=count+1;
                end
            end
        end
        
        function does_contain = contains_key(obj,my_key)
            
            [hash_index,key_index] = obj.get_key_index(my_key);
            does_contain = key_index <= length(obj.my_key_table{hash_index});
            
        end
    end
end