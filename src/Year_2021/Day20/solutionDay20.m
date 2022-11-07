function solutionDay20()

%parse the input
fid = fopen('InputDay20a.txt');
data = textscan(fid,'%s');
data = data{1};
fclose(fid);

picture_array = zeros(length(data),length(data{1}));
for i = 1:length(data)
    for j = 1:length(data{1})
        picture_array(i,j)=data{i}(j)=='#';
    end
end

fid = fopen('InputDay20b.txt');
data = textscan(fid,'%s');
data = data{1}{1};
fclose(fid);

conversion_map = data =='#';
 
compute_iteration_pictures(picture_array,conversion_map,2);
compute_iteration_pictures(picture_array,conversion_map,50);
end

function compute_iteration_pictures(picture_array,conversion_map,num_iterations)
    convolve_matrix = [[256,128,64];[32,16,8];[4,2,1]];

    infinity_bit = 0;

    for count = 1:num_iterations
        picture_array = pad_array(picture_array,2,infinity_bit);

        new_picture_array = zeros(size(picture_array));
        for i=2:(size(picture_array,1)-1)
            for j=2:(size(picture_array,2)-1)
                new_picture_array(i,j) = conversion_map(sum(sum(picture_array((i-1):(i+1),(j-1):(j+1)).*convolve_matrix))+1);
            end
        end
        infinity_bit = conversion_map(511*infinity_bit+1);
        
        new_picture_array = set_rim_values(new_picture_array,infinity_bit);
        picture_array = new_picture_array;
    end
    disp(['number of lit bits: ',num2str(sum(sum(picture_array)))])
end

function picture_array = pad_array(picture_array,pad_size,bit_val)
    s=size(picture_array);
    picture_array = [bit_val*ones(s(1)+2*pad_size,pad_size), [bit_val*ones(pad_size,s(2));picture_array;bit_val*ones(pad_size,s(2))] , bit_val*ones(s(1)+2*pad_size,pad_size)];
end

function picture_array = set_rim_values(picture_array,bit_val)
    picture_array(:,1)=bit_val;
    picture_array(:,end)=bit_val;
    picture_array(1,:)=bit_val;
    picture_array(end,:)=bit_val;
end

