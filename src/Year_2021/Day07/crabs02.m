function res=submarine01()
q = importdata('InputDay07.dat');

q=sort(q);

fuel_listA = zeros(1,length(q));

fuel_listA(1)=sum(q-q(1));

count_decrease = 1;
count_increase = length(q)-1;

for i = 2:length(q)
    fuel_listA(i) = fuel_listA(i-1) + (q(i)-q(i-1))*(count_decrease-count_increase);
    count_decrease = count_decrease+1;
    count_increase = count_increase-1;
end

a = length(q);
b = sum(-2*q);
c = sum(q.^2);


fuel_listB = a*q.^2+b*q+c;

fuel_list = fuel_listA+fuel_listB;

min(fuel_list)/2



end