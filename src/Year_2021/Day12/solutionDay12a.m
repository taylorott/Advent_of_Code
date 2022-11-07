function res=submarine01()

fid = fopen('InputDay12.txt');
data = textscan(fid,'%s');
fclose(fid);


num_lines = length(data{1});

my_array = [];

num_columns = 0;

my_string_list = {};

adjacency_mat = [];
start_index = 0;
end_index = 0;

cave_size = [];

for i = 1:num_lines
    string_list  = strsplit(data{1}{i},'-');
    
    str1 = string_list{1};
    str2 = string_list{2};
    
    index1 = get_string_index(my_string_list, str1);
    my_string_list{index1} = str1;
    
    index2 = get_string_index(my_string_list, str2);
    my_string_list{index2} = str2;
    
    adjacency_mat(index1,index2) = 1;
    adjacency_mat(index2,index1) = 1;
    
    if strcmp(str1,'start')
        start_index = index1;
    end
    
    if strcmp(str2,'start')
        start_index = index2;
    end
    
    if strcmp(str1,'end')
        end_index = index1;
    end
    
    if strcmp(str2,'end')
        end_index = index2;
    end
    
    if 'a'<=str1(1) && str1(1)<='z'
        cave_size(index1) = 0;
    else
        cave_size(index1) = 1;
    end

    if 'a'<=str2(1) && str2(1)<='z'
        cave_size(index2) = 0;
    else
        cave_size(index2) = 1;
    end
end

cave_size(start_index) = 0;
cave_size(end_index) = 2;



small_cave_index = find(cave_size == 0);

adjacency_list = {};
for i = 1:length(my_string_list)
    adjacency_list{i} = find(adjacency_mat(:,i));
end

path_list_current = {[start_index]};
path_list_terminated = {};

while length(path_list_current)>0
    path_list_new = {};
    
    for i = 1:length(path_list_current)
        current_path = path_list_current{i};
        last_step = path_list_current{i}(end);
        for j = 1:length(adjacency_list{last_step})
            possible_step = adjacency_list{last_step}(j);
            if cave_size(possible_step)==0
                if ~ismember(possible_step,path_list_current{i})
                    path_list_new{end+1} = [path_list_current{i},possible_step];
                end
            end
            
            if cave_size(possible_step)==1
                path_list_new{end+1} = [path_list_current{i},possible_step];
            end
            
            if cave_size(possible_step)==2
                path_list_terminated{end+1} = [path_list_current{i},possible_step];
            end
        end
    end
    
    path_list_current = path_list_new;
end
length(path_list_terminated)


end

function res = get_string_index(string_list, string_in)
    res = length(string_list)+1;
    
    for i = 1:length(string_list)
        if strcmp(string_list{i},string_in)
            res = i;
        end
    end
   
    
end