function res=submarine01()
 
q = importdata('InputDay01.dat');

count = 0
for i = 1:(length(q)-3)
    if q(i+3)>q(i)
       count=count+1; 
    end
end
count


end