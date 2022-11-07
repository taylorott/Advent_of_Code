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



for i = 1:num_lines
    my_str = data{1}{i};
    a=my_str(1)-'A'+1;
    b=my_str(2)-'A'+1;
    c=my_str(end)-'A'+1;

    char_list(a)=1;
    char_list(b)=1;
    char_list(c)=1;
end


char_index = cumsum(char_list);
num_chars = sum(char_list);
convert_mat = zeros(num_chars,num_chars);

for i = 1:num_lines
    my_str = data{1}{i};
    a=my_str(1)-'A'+1;
    b=my_str(2)-'A'+1;
    c=my_str(end)-'A'+1;
    convert_mat(char_index(a),char_index(b))=char_index(c);
end

for i=1:length(current_polymer)
    current_polymer(i)=char_index(current_polymer(i));
end

% convert_mat
% current_polymer
% num_chars

super_convert = zeros(num_chars^2,num_chars^2);

for i = 1:num_chars
    for j = 1:num_chars
        if convert_mat(i,j)~=0
            k = convert_mat(i,j);
            my_indexA=(i-1)*num_chars+j;
            my_indexB=(i-1)*num_chars+k;
            my_indexC=(k-1)*num_chars+j;
            super_convert(my_indexB,my_indexA)=1;
            super_convert(my_indexC,my_indexA)=1;
        end  
    end
end

current_vec = zeros(num_chars^2,1);

for i=1:(length(current_polymer)-1)
    my_indexA=(current_polymer(i)-1)*num_chars+current_polymer(i+1);
    current_vec(my_indexA)=current_vec(my_indexA)+1;
end

for i = 1:40
    current_vec=super_convert*current_vec;
end

char_count=zeros(num_chars,1);
char_count(current_polymer(1))=.5;
char_count(current_polymer(end))=.5;
for i = 1:num_chars
    for j = 1:num_chars
        my_indexA=(i-1)*num_chars+j;
        char_count(i) = char_count(i) + current_vec(my_indexA)/2;
        char_count(j) = char_count(j) + current_vec(my_indexA)/2;
    end
end

sorted_char_count = sort(char_count);
sorted_char_count(end)-sorted_char_count(1)

end

