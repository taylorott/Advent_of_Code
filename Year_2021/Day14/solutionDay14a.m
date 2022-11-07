function res=submarine01()

fid = fopen('InputDay14a.txt');
data = textscan(fid,'%s');
fclose(fid);

my_str = data{1}{1};
current_polymer = [];
char_list = zeros(26,1);

for i = 1:length(my_str)
    current_polymer(i)=my_str(i)-'A'+1;
    char_list(my_str(i)-'A'+1)=1;
end


fid = fopen('InputDay14b.txt');
data = textscan(fid,'%s','Delimiter',{'\n'});
fclose(fid);

num_lines = length(data{1});
convert_mat = zeros(26,26);


for i = 1:num_lines
    my_str = data{1}{i};
    a=my_str(1)-'A'+1;
    b=my_str(2)-'A'+1;
    c=my_str(end)-'A'+1;
    convert_mat(a,b)=c;
    char_list(a)=1;
    char_list(b)=1;
    char_list(c)=1;
end



convert_mat
current_polymer

for count=1:10
    new_polymer=[];
    for i = 1:(length(current_polymer)-1)
        new_polymer(end+1)=current_polymer(i);
        if convert_mat(current_polymer(i),current_polymer(i+1))~=0
            new_polymer(end+1)=convert_mat(current_polymer(i),current_polymer(i+1));
        end
    end
    
    new_polymer(end+1)=current_polymer(end);
    current_polymer=new_polymer;
end

char_count_list = [];
for i=1:26
   if char_list(i)
       char_count_list(end+1)=sum(current_polymer==i);
   end
end
sorted_char_count_list=sort(char_count_list);
sorted_char_count_list(end)-sorted_char_count_list(1)

end

