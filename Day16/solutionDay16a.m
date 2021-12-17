function res=submarine01()

fid = fopen('InputDay16.txt');
data = textscan(fid,'%s');
fclose(fid);

my_str = data{1}{1};

% binVal = hexToBinaryVector(data{1}{1})

combined_bit_string = [];
for i = 1:length(my_str)
    current_char = my_str(i);
    bit_string = hexToBinaryVector(current_char);
    bit_string = [zeros(1,4-length(bit_string)),bit_string];
    combined_bit_string((end+1):(end+4)) = bit_string;
end

% combined_bit_string

myTree = PacketTree();
my_remainder = myTree.decode_packet(combined_bit_string);

% myTree.literal_value

myTree.get_version_tree_sum()
myTree.packet_value
end


