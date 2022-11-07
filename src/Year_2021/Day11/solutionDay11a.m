function res=submarine01()

fid = fopen('InputDay11.txt');
data = textscan(fid,'%s');
fclose(fid);


num_lines = length(data{1});

my_array = [];

num_columns = 0;
for i = 1:num_lines
    my_string = data{1}{i};
    num_columns = length(my_string);

    for j = 1:length(my_string)
        my_array(i,j)=str2num(my_string(j));
        
    end
end



my_array = [zeros(1,num_columns+2);[zeros(num_lines,1),my_array,zeros(num_lines,1)];zeros(1,num_columns+2)];



num_flashes = 0;

num_columns

for n = 1:100
    my_array(2:(num_lines+1),2:(num_columns+1))
    
    
    my_array = my_array+1;
    
    run_flashes = 1;
    
    flash_count = 1;
    flash_array = zeros(num_lines+2,num_columns+2);
    while run_flashes == 1
        run_flashes = 0;
        
        for i = 2:(num_lines+1)
            for j = 2:(num_columns+1)
                if my_array(i,j)>9 && flash_array(i,j)==0
                    num_flashes = num_flashes+1;
                    flash_array(i,j)=flash_count;
                    run_flashes=1;
                end
            end
        end

        for i = 2:(num_lines+1)
            for j = 2:(num_columns+1)
                if flash_array(i,j)==flash_count
                    my_array(i+1,j+1)   =my_array(i+1,j+1)+1;
                    my_array(i+1,j)     =my_array(i+1,j)+1;
                    my_array(i+1,j-1)   =my_array(i+1,j-1)+1;
                    my_array(i,j+1)     =my_array(i,j+1)+1;
                    my_array(i,j-1)     =my_array(i,j-1)+1;
                    my_array(i-1,j+1)   =my_array(i-1,j+1)+1;
                    my_array(i-1,j)     =my_array(i-1,j)+1;
                    my_array(i-1,j-1)   =my_array(i-1,j-1)+1;
                end
            end
        end
        flash_count = flash_count+1;    
    end
    for i = 2:(num_lines+1)
       for j = 2:(num_columns+1)
            if flash_array(i,j)>0
                my_array(i,j)=0;
            end
       end
    end
    
end

num_flashes

end