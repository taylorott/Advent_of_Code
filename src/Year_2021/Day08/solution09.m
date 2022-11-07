function res=submarine01()

fid = fopen('InputDay08.txt');
data = textscan(fid,'%s');
fclose(fid);


num_cases = length(data{1});

final_mat = []
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
    temp_sum = sum(charMat1,2);
    
    temp_sum;
    vec1 = charMat1(find(temp_sum==2),:);
    vec7 = charMat1(find(temp_sum==3),:);
    vec4 = charMat1(find(temp_sum==4),:);
    vec8 = charMat1(find(temp_sum==8),:);
    
    sigmat = [temp_sum,charMat1*vec1',charMat1*vec4'];
    sorted_mat = zeros(10,7);
    for j=1:10
        my_switch = -1;
        
        if sigmat(j,1)==2
            my_switch = 1;
        end
        
        if sigmat(j,1)==3
            my_switch = 7;
        end
        
        if sigmat(j,1)==4
            my_switch = 4;
        end
        
        if sigmat(j,1)==7
            my_switch = 8;
        end
                
        if sigmat(j,1)==6 && sigmat(j,2)==2 && sigmat(j,3)==3
            my_switch = 0;
        end

        if sigmat(j,1)==6 && sigmat(j,2)==2 && sigmat(j,3)==4
            my_switch = 9;
        end
        
        if sigmat(j,1)==6 && sigmat(j,2)==1 
            my_switch = 6;
        end

        if sigmat(j,1)==5 && sigmat(j,2)==2
            my_switch = 3;
        end

        if sigmat(j,1)==5 && sigmat(j,2)==1 && sigmat(j,3)==2
            my_switch = 2;
        end
        
        if sigmat(j,1)==5 && sigmat(j,2)==1 && sigmat(j,3)==3
            my_switch = 5;
        end

        my_switch=my_switch+1;
        
        sorted_mat(my_switch,:)=charMat1(j,:);
    end
    

    for j=1:4
        for k=1:10
            if sum(charMat2(j,:)==sorted_mat(k,:))==7
                final_mat(i,j)=k-1;
            end
        end
    end
    
%     temp = sum(charMat2,2)
%     
%     total = total + sum((temp==2) + (temp==3) + (temp==4) + (temp==7));
end

sum(sum(final_mat).*(10.^[3,2,1,0]))

% total



end