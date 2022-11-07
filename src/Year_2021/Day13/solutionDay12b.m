function res=submarine01()

fid = fopen('InputDay13a.txt');
data = textscan(fid,'%s');
fclose(fid);

num_lines = length(data{1});

dot_coords = [];
for i = 1:num_lines
    string_list  = strsplit(data{1}{i},',');
    
    str1 = string_list{1};
    str2 = string_list{2};
    
    dot_coords(i,1)=str2num(str1);
    dot_coords(i,2)=str2num(str2);
    
end

fid = fopen('InputDay13b.txt');
data = textscan(fid,'%s','Delimiter',{'\n'});
fclose(fid);

num_lines = length(data{1});
fold_list = [];
fold_type_list = [];
for i = 1:num_lines
    
    string_list1  = strsplit(data{1}{i},'=');

    str1 = string_list1{1};
    str2 = string_list1{2};

    fold_list(i)=str2num(str2);
    
    if str1(end)=='x'
        fold_type_list(i)=0;
    else
        fold_type_list(i)=1;
    end
    
end



for i = 1:length(fold_list);
    num_points = max(size(dot_coords))
    if fold_type_list(i)==0
        for j = 1:num_points
            dot_coords(j,1) = fold(dot_coords(j,1),fold_list(i));
        end
    else
        for j = 1:num_points
            dot_coords(j,2) = fold(dot_coords(j,2),fold_list(i));
        end
    end 

    dot_coords = delete_duplicates(dot_coords);
end

num_points = max(size(dot_coords));

my_mat = [];
for i = 1:num_points
    my_mat(dot_coords(i,1)+1,dot_coords(i,2)+1)=1;
end
my_mat = my_mat'
end

function new_dot_coords = delete_duplicates(dot_coords)
 
    [~,I] = sort(dot_coords(:,1));
    dot_coords = dot_coords(I,:);

    
    num_points = max(size(dot_coords));
    
    count1=1;
    count2=1;
    
    while count1<num_points
        count2=count2+1;
        if count2>num_points || dot_coords(count1,1)~=dot_coords(count2,1)
            
            dot_coords(count1:(count2-1),2)=sort(dot_coords(count1:(count2-1),2));
            
  
            
            
            count1=count2;
        end
    end
    

    
    new_dot_coords = dot_coords(1,:);
    count=1;
    for i=2:num_points
        if  dot_coords(i,1)~=new_dot_coords(count,1) || dot_coords(i,2)~=new_dot_coords(count,2)
            count=count+1;
            new_dot_coords(count,:)=dot_coords(i,:);
        end
    end
end

function res = fold(point_coord,fold_number)
    res = point_coord;
    if point_coord>fold_number
        res = fold_number - (point_coord - fold_number);
    end
end