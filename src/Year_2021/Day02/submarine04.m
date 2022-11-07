function res=submarine01()
 
q = importdata('InputDay02.dat')

depth = 0
distance = 0
aim = 0

for i=1:length(q.data)
   if strcmp(q.textdata{i},'forward')
       distance = distance+q.data(i);
       depth = depth+aim*q.data(i);
   end
   
   if strcmp(q.textdata{i},'down')
       aim = aim+q.data(i);
   end
   
  if strcmp(q.textdata{i},'up')
       aim = aim-q.data(i);
  end
   
end

format longG

depth
distance
depth*distance


end