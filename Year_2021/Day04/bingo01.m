function res=submarine01()
q1 = importdata('InputDay04a.dat');
q2 = importdata('InputDay04b.dat');

boards_list = zeros(5,5,0);

for i = 0:((length(q1(:,1))/5)-1)
    boards_list(:,:,i+1) = q1((5*i+1):(5*i+5),1:5);
end

marked = zeros(size(boards_list));

count = 1;
while sum(sum((sum(marked)==5)))+sum(sum(sum(marked,2)==5)) == 0
    marked = marked + (boards_list==q2(count));
    count = count + 1;
end

%
find(sum(marked)==5)
board_index = floor(find(sum(marked,2)==5)/5);
sum(sum(boards_list(:,:,board_index).*(1-marked(:,:,board_index))))*q2(count-1)

end