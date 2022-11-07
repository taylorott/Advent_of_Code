function res=submarine01()

fid = fopen('InputDay09.txt');
data = textscan(fid,'%s');
fclose(fid);


my_height = length(data{1});
my_width = length( data{1}{1});

for i = 1:my_height
    q =  data{1}{i};
   for j = 1:my_width
       my_array(i,j) = str2num(q(j));
   end
end

my_array = [9*ones(1,my_width);my_array;9*ones(1,my_width)];
my_array = [9*ones(my_height+2,1),my_array,9*ones(my_height+2,1)];


total = 0;
for i = 2:(my_height+1)
    for j = 2:(my_width+1)
        if my_array(i,j)<min([my_array(i-1,j),my_array(i+1,j),my_array(i,j-1),my_array(i,j+1)])
            total = total+(my_array(i,j)+1);
        end
    end
end

total
% q = importdata('InputDay09.dat');

% size(q)




end