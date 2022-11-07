function res=submarine01()
fid = fopen('InputDay03.txt');
data = textscan(fid,'%s');
fclose(fid);

my_bin_array = []

for i = 1:length(data{1})
    for j = 1:length(data{1}{i})
       my_bin_array(i,j) = str2num(data{1}{i}(j));
    end    
end

oxygen_array = my_bin_array;
co2_array = my_bin_array;

b_string_length = length(oxygen_array(1,:));

bit_index = 1;
while length(oxygen_array(:,1))>1
    q = sum(oxygen_array)>=length(oxygen_array(:,1))/2;
    new_oxygen_array = zeros(0,b_string_length);
    for i = 1:length(oxygen_array(:,1))
       if oxygen_array(i,bit_index)==q(bit_index)
           new_oxygen_array(end+1,:)=oxygen_array(i,:);
       end
    end
    oxygen_array = new_oxygen_array;  
    bit_index = bit_index+1;
end

bit_index = 1;
while length(co2_array(:,1))>1
    q = sum(co2_array)<length(co2_array(:,1))/2;
    new_co2_array = zeros(0,b_string_length);
    for i = 1:length(co2_array(:,1))
       if co2_array(i,bit_index)==q(bit_index)
           new_co2_array(end+1,:)=co2_array(i,:);
       end
    end
    co2_array = new_co2_array ;  
    bit_index = bit_index+1;
end

oxygen_array
co2_array
% q = sum(my_bin_array)>length(my_bin_array(:,1))/2;
% p = ~q;
% 
sum((2.^((length(oxygen_array)-1):-1:0)).*oxygen_array)*sum((2.^((length(co2_array)-1):-1:0)).*co2_array)

end