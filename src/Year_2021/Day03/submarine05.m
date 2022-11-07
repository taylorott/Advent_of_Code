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

q = sum(my_bin_array)>length(my_bin_array(:,1))/2;
p = ~q;

sum((2.^((length(p)-1):-1:0)).*q)*sum((2.^((length(p)-1):-1:0)).*p)

end