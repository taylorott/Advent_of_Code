classdef OrionPriorityQueue < handle
    properties
        priority_queue_index_map;
        my_key_queue;
        my_value_queue;
        num_keys;
    end
    
    methods
        function obj = OrionPriorityQueue(m)
            obj.num_keys = 0;
            obj.my_key_queue = {};
            obj.my_value_queue = [];
            obj.priority_queue_index_map = OrionHashTable(m);
        end
        
        function consistent_bool = test_table_validity(obj)
            consistent_bool = 1;
            for i = 1:obj.num_keys
                current_key = obj.my_key_queue{i};
                temp_key_info = obj.priority_queue_index_map.get_value(current_key);
                current_index = temp_key_info(1);
                if current_index~=i
                    consistent_bool = 0;
                end
%                 old_value = temp_key_info(2);
            end
        end
        
        function num_keys = num_elements(obj)
            num_keys = obj.num_keys;
        end
        
        function [key_out,value_out] = pop(obj)
            %pull out the key and value at the top of the queue
            key_out = obj.my_key_queue{1};
            value_out = obj.my_value_queue(1);
            
%             priority_queue_index_list(key_out)=0;
%             obj.priority_queue_index_map.update_value(key_out,[0,value_out]);
            obj.priority_queue_index_map.delete_key(key_out);
            
            if obj.num_keys>1
                obj.my_key_queue{1} = obj.my_key_queue{obj.num_keys};
                obj.my_value_queue(1) = obj.my_value_queue(obj.num_keys);
                obj.priority_queue_index_map.update_value(obj.my_key_queue{1},[1,obj.my_value_queue(1)]);
    %             priority_queue_index_list(obj.my_key_queue{1})=1;
            end

            obj.num_keys = obj.num_keys -1;
            obj.sift_down_from_top();
        end
        
        function value_out = get_key_value(obj,key_in)
            temp_key_info = obj.priority_queue_index_map.get_value(key_in);
            current_index = temp_key_info(1);
            value_out = temp_key_info(2);
        end

        function push(obj,key_in,value_in)
            obj.num_keys = obj.num_keys + 1;
            current_index  = obj.num_keys;
            
            obj.my_key_queue{current_index}= key_in;
            obj.my_value_queue(current_index) = value_in;
            
            
%             priority_queue_index_list(obj.my_key_queue{current_index})=current_index;
            obj.priority_queue_index_map.insert(key_in,[current_index,value_in]);

            obj.sift_up_from_index(current_index);
        end
        
        %only operates if new value is less than old value
        function decrement_key(obj,key_in,value_in)
            
%             current_index  = index_to_fix;
            temp_key_info = obj.priority_queue_index_map.get_value(key_in);
            current_index = temp_key_info(1);
            old_value = temp_key_info(2);
%             disp(['key matches: ',num2str(prod(obj.my_key_queue{current_index}==key_in))]);
            if value_in<old_value
                obj.priority_queue_index_map.update_value(key_in,[current_index,value_in]);
                obj.my_value_queue(current_index) = value_in;
                
                obj.sift_up_from_index(current_index);
            end
        end
        
        function sift_up_from_index(obj,current_index)
            switch_index = floor((current_index-2)/2)+1;
            while switch_index>=1 && obj.my_value_queue(current_index)<obj.my_value_queue(switch_index)
                
                temp_key = obj.my_key_queue{current_index};
                obj.my_key_queue{current_index}= obj.my_key_queue{switch_index};
                obj.my_key_queue{switch_index} = temp_key;
                
                temp_value = obj.my_value_queue(current_index);
                obj.my_value_queue(current_index) = obj.my_value_queue(switch_index);
                obj.my_value_queue(switch_index) = temp_value;


                obj.priority_queue_index_map.update_value(obj.my_key_queue{current_index},[current_index,obj.my_value_queue(current_index)]);                
                obj.priority_queue_index_map.update_value(obj.my_key_queue{switch_index},[switch_index,obj.my_value_queue(switch_index)]);
                
                current_index = switch_index;
                switch_index = floor((current_index-2)/2)+1;
            end
        end
        
        function sift_down_from_top(obj)
            current_index = 1;
            while (current_index-1)*2+2 <= obj.num_keys
                index_left = (current_index-1)*2+2;
                index_right = (current_index-1)*2+3;
                switch_index = -1;

                if index_right <= obj.num_keys
                    if obj.my_value_queue(current_index)<obj.my_value_queue(index_left)&&...
                       obj.my_value_queue(current_index)<obj.my_value_queue(index_right)
                        break
                    else
                        if obj.my_value_queue(index_left)<obj.my_value_queue(index_right)
                            switch_index = index_left;
                        else
                            switch_index = index_right;
                        end
                    end
                else
                    if obj.my_value_queue(current_index)<obj.my_value_queue(index_left)
                        break
                    else
                        switch_index = index_left;
                    end
                end
                temp_key = obj.my_key_queue{switch_index};
                obj.my_key_queue{switch_index} = obj.my_key_queue{current_index};
                obj.my_key_queue{current_index}= temp_key;
                
                temp_value = obj.my_value_queue(switch_index);
                obj.my_value_queue(switch_index) = obj.my_value_queue(current_index);
                obj.my_value_queue(current_index) = temp_value;

                obj.priority_queue_index_map.update_value(obj.my_key_queue{current_index},[current_index,obj.my_value_queue(current_index)]);
                obj.priority_queue_index_map.update_value(obj.my_key_queue{switch_index},[switch_index,obj.my_value_queue(switch_index)]);
%                 priority_queue_index_list(obj.my_key_queue{switch_index})=switch_index;
%                 priority_queue_index_list(obj.my_key_queue{current_index})=current_index;

                current_index = switch_index;
            end 
        end
        

    
    end
end