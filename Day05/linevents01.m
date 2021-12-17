function res=submarine01()
fid = fopen('InputDay05.txt');
data = textscan(fid,'%s');
fclose(fid);

num_entries = length(data{1})/3;

for i = 1:num_entries
    C = strsplit(data{1}{3*(i-1)+1},',');
    q(i,1) = str2num(C{1});
    q(i,2) = str2num(C{2});
    
    C = strsplit(data{1}{3*(i-1)+3},',');
    q(i,3) = str2num(C{1});
    q(i,4) = str2num(C{2});
end

my_grid = zeros(1000,1000);

for i=1:num_entries
   if q(i,1)==q(i,3) || q(i,2)==q(i,4) 
       my_grid(min(q(i,[1,3])):max(q(i,[1,3])),min(q(i,[2,4])):max(q(i,[2,4])))...
           =my_grid(min(q(i,[1,3])):max(q(i,[1,3])),min(q(i,[2,4])):max(q(i,[2,4])))+1;
   end
end

sum(sum(my_grid>1))

end