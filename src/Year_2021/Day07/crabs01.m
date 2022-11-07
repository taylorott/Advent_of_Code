function res=submarine01()
q = importdata('InputDay07.dat');

q=sort(q);

fuel_list = zeros(1,length(q));

fuel_list(1)=sum(q-q(1));

count_decrease = 1;
count_increase = length(q)-1;

for i = 2:length(q)
    fuel_list(i) = fuel_list(i-1) + (q(i)-q(i-1))*(count_decrease-count_increase);
    count_decrease = count_decrease+1;
    count_increase = count_increase-1;
end

min(fuel_list)


end