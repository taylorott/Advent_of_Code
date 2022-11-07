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



count = 0;
my_coord_list = [];

basin_labels = 0*my_array;
basin_count_list = [];

function basin_total = check_basin(x1,y1)
    basin_total = 0;
    if 2<=x1 && x1<=(my_height+1) && 2<=y1 && y1<=(my_width+1) && basin_labels(x1,y1)==0 && my_array(x1,y1)~=9
        basin_total=1;
        basin_labels(x1,y1)=1;
        basin_total = basin_total+check_basin(x1+1,y1);
        basin_total = basin_total+check_basin(x1-1,y1);
        basin_total = basin_total+check_basin(x1,y1+1);
        basin_total = basin_total+check_basin(x1,y1-1);
    end
end


for i = 2:(my_height+1)
    for j = 2:(my_width+1)
        if my_array(i,j)<min([my_array(i-1,j),my_array(i+1,j),my_array(i,j-1),my_array(i,j+1)])
            my_coord_list= [my_coord_list;[i,j]];
            count = count+1;
            
            basin_count_list(count) = check_basin(i,j);
        end
    end
end


q = sort(basin_count_list);
q(end)*q(end-1)*q(end-2)

% my_coord_list
% q = importdata('InputDay09.dat');

% size(q)




end