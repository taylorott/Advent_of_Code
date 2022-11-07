function solutionDay18()

%parse the input
fid = fopen('InputDay18.txt');
data = textscan(fid,'%s');
fclose(fid);

num_input_lines = length(data{1});


mySnailfishNumber1 = SnailfishNumber();
% mySnailfishNumber1.debugflag = 1;
mySnailfishNumber1.UnpackString(data{1}{1});

for i = 2:num_input_lines

    input_string =  data{1}{i};
    mySnailfishNumber2 = SnailfishNumber();
    mySnailfishNumber2.UnpackString(input_string);
    mySnailfishNumber1 = mySnailfishNumber1.addOperation(mySnailfishNumber2);

end

mySnailfishNumber1.compute_magnitude()
% mySnailfishNumber1.generate_SnailfishNumber_string()

max_magnitude = 0;

for i = 1:num_input_lines
    for j = 1:num_input_lines
        if i~=j
            mySnailfishNumber1 = SnailfishNumber();
            mySnailfishNumber1.UnpackString(data{1}{i});
            
            mySnailfishNumber2 = SnailfishNumber();
            mySnailfishNumber2.UnpackString(data{1}{j});
            
            mySnailfishNumber3 = mySnailfishNumber1.addOperation(mySnailfishNumber2);
            possible_mag = mySnailfishNumber3.compute_magnitude();
            
            if possible_mag>max_magnitude
                max_magnitude = possible_mag;
            end
        end
    end
end

max_magnitude
end