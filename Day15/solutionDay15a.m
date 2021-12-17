function res=submarine01()

fid = fopen('InputDay15.txt');
data = textscan(fid,'%s');
fclose(fid);

my_height = length(data{1});
my_width = length(data{1}{1});

my_mat=[];
for i =1:my_height
    my_str = data{1}{i};
    for j = 1:length(my_str)
        my_mat(i,j) = str2num(my_str(j));
    end
end


num_vertices = my_height*my_width;

my_adjacency = zeros(num_vertices,num_vertices);

for i = 1:my_height
    for j = 1:my_width
        my_index1 = j+(i-1)*my_height;
        
        if i>1
            a = i-1;
            b = j;
            my_index2 = b+(a-1)*my_height;
            my_adjacency(my_index1,my_index2) = my_mat(a,b);
            my_adjacency(my_index2,my_index1) = my_mat(i,j);
        end
        
        if i<my_height
            a = i+1;
            b = j;
            my_index2 = b+(a-1)*my_height;
            my_adjacency(my_index1,my_index2) = my_mat(a,b);
            my_adjacency(my_index2,my_index1) = my_mat(i,j);
        end
        
        if j>1
            a = i;
            b = j-1;
            my_index2 = b+(a-1)*my_height;
            my_adjacency(my_index1,my_index2) = my_mat(a,b);
            my_adjacency(my_index2,my_index1) = my_mat(i,j);
        end
        
        if j<my_width
            a = i;
            b = j+1;
            my_index2 = b+(a-1)*my_height;
            my_adjacency(my_index1,my_index2) = my_mat(a,b);
            my_adjacency(my_index2,my_index1) = my_mat(i,j);
        end
    end
end

my_Graph = digraph(my_adjacency);


% my_height
% my_width
% 
% my_mat

% G = digraph([1 2],[2 3])
% my_mat


[P,d] = shortestpath(my_Graph,1,num_vertices);

d




end

