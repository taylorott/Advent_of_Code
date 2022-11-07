function res=submarine01()
q = importdata('InputDay06.dat')

fishlist = []
mq = max(q)
for i=1:mq
    fishlist(i+1)=sum(q==i);
end

fishlist(9) = 0;

for i=1:80
   templist = zeros(1,9);
   templist(7)=fishlist(1);
   fishlist = [fishlist(2:9),fishlist(1)] + templist;
end

sum(fishlist)