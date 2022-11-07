function res=submarine01()

fid = fopen('InputDay08.txt');
data = textscan(fid,'%s');
fclose(fid);


num_cases = length(data{1});

total = 0;
for i = 1:num_cases
    C=strsplit(data{1}{i},'|');
    q1=strsplit(C{1},',');
    q2=strsplit(C{2},',');
 
    charMat1=zeros(10,7);
    for j=1:10
        for k=1:length(q1{j})
            q1{j}(k)-'a'+1;
            charMat1(j,q1{j}(k)-'a'+1)=1;
        end
    end
    
    charMat2=zeros(4,7);
    for j=2:5
        for k=1:length(q2{j})
            q2{j}(k)-'a'+1;
            charMat2(j-1,q2{j}(k)-'a'+1)=1;
        end
    end
    
    temp = sum(charMat2,2)
    
    total = total + sum((temp==2) + (temp==3) + (temp==4) + (temp==7));
end

total



end