function res=submarine01()
q1 = importdata('InputDay04a.dat');
q2 = importdata('InputDay04b.dat');

boards_list = zeros(5,5,0);

for i = 0:((length(q1(:,1))/5)-1)
    boards_list(:,:,i+1) = q1((5*i+1):(5*i+5),1:5);
end

marked = zeros(size(boards_list));

count = 1;
while length(marked(1,1,:))>1
    marked = marked + (boards_list==q2(count));
    count = count + 1;
    
    new_marked = zeros(5,5,0);
    new_boards_list = zeros(5,5,0);
    
    for i = 1:length(marked(1,1,:))
        if ~(sum(sum(marked(:,:,i))==5)>0 || sum(sum(marked(:,:,i),2)==5)>0)
            new_marked(:,:,end+1)=marked(:,:,i);
            new_boards_list(:,:,end+1)=boards_list(:,:,i);
        end
    end
    marked = new_marked;
    boards_list = new_boards_list;
end

while sum(sum((sum(marked)==5)))+sum(sum(sum(marked,2)==5)) == 0
    marked = marked + (boards_list==q2(count));
    count = count + 1;
end

sum(sum((1-marked).*boards_list))*q2(count-1)

end