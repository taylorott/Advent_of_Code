function res=submarine01()
 
q = importdata('InputDay02.dat')

depth = 0
distance = 0


for i=1:length(q.data)
   if strcmp(q.textdata{i},'forward')
       distance = distance+q.data(i)
   end
   
   if strcmp(q.textdata{i},'down')
       depth = depth+q.data(i)
   end
   
  if strcmp(q.textdata{i},'up')
       depth = depth-q.data(i)
  end
   
end

depth*distance


end