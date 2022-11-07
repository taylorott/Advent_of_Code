classdef PacketTree < handle
    
        properties
            version;
            ID;
            operator;
            is_literal;
            literal_value;
            subpacket_list;
            subpacket_value_list;
            packet_value;
        end
        
        methods
            
            function obj = PacketTree()

            end
            
            function my_remainder = decode_packet(obj,bit_string)
                [version,ID,my_remainder] = obj.unpack_packet(bit_string);
                obj.version = version;
                obj.ID = ID;
                
                if obj.ID == 4
                    obj.is_literal = 1;
                    [number_out,my_remainder] = obj.decode_literal(my_remainder);

                    obj.literal_value = number_out;
                    obj.packet_value = number_out;
                else
                    obj.is_literal = 0;
                    [subpacket_list , my_remainder, subpacket_value_list] = obj.decode_operator(my_remainder);
                    obj.subpacket_value_list = subpacket_value_list;
                    obj.subpacket_list=subpacket_list;
                    obj.packet_value = obj.evaluate_operator(obj.ID,obj.subpacket_value_list);
                end
            end
            
            function my_value = evaluate_operator(obj,my_ID,my_value_list)
                my_value = 0;
                if my_ID ==0
                    my_value = sum(my_value_list);
                end
                if my_ID ==1
                    my_value = prod(my_value_list);
                end
                if my_ID ==2
                    my_value = min(my_value_list);
                end
                if my_ID ==3
                    my_value = max(my_value_list);
                end
                if my_ID ==5
                    my_value = my_value_list(1)>my_value_list(2);
                end
                if my_ID ==6
                    my_value = my_value_list(1)<my_value_list(2);
                end
                if my_ID ==7
                    my_value = my_value_list(1)==my_value_list(2);
                end
            end
            
            function version_sum = get_version_tree_sum(obj)
                version_sum = obj.version;
                if obj.is_literal==0
                    for i = 1:length(obj.subpacket_list)
                        version_sum = version_sum+obj.subpacket_list{i}.get_version_tree_sum();
                    end
                end
            end
      
            function [version,ID,my_remainder] = unpack_packet(obj,bit_string)
                version = sum([4,2,1].*bit_string(1:3));
                ID = sum([4,2,1].*bit_string(4:6));
                my_remainder = bit_string(7:end);
            end

            function [number_out,my_remainder] = decode_literal(obj,bit_string)
                relevant_bit_string = [];

                terminate_flag = 0;
                count = 0;
                while terminate_flag == 0
                    bit_substring = bit_string((count+1):(count+5));
                    if bit_substring(1)==0
                        terminate_flag = 1;
                    end
                    relevant_bit_string((end+1):(end+4))=bit_substring(2:5);
                    count = count+5;
                end

                my_remainder = bit_string((count+1):end);
                number_out = obj.myBin2Dec(relevant_bit_string);
            end

            function [subpacket_list , my_remainder, subpacket_value_list] = decode_operator(obj,bit_string)
                my_mode = bit_string(1);
                subpacket_list = {};
                subpacket_value_list = [];
                my_remainder = [];

                if my_mode ==0
                    sub_packet_length = obj.myBin2Dec(bit_string(2:16));                    
                    subpacket_string = bit_string(17:(16+sub_packet_length));
                    
                    my_remainder = bit_string((16+sub_packet_length+1):end);
                    while length(subpacket_string)>0
                        subpacket_list{end+1} = PacketTree();
                        subpacket_string = subpacket_list{end}.decode_packet(subpacket_string);
                        subpacket_value_list(end+1) = subpacket_list{end}.packet_value;
                    end
                else
                    num_packets = obj.myBin2Dec(bit_string(2:12));
                    my_remainder = bit_string(13:end);
                    count = 1;
                    while count<=num_packets
                        subpacket_list{end+1} = PacketTree();
                        my_remainder = subpacket_list{end}.decode_packet(my_remainder);
                        subpacket_value_list(end+1) = subpacket_list{end}.packet_value;
                        count = count+1;
                    end
                end
            end

            function number_out = myBin2Dec(~,bit_string)
                number_out = sum((2.^((length(bit_string)-1):-1:0)).*bit_string);
            end
   end
end
