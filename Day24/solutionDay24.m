function solutionDay24()

    %parse the input
    fid = fopen('InputDay24.txt');
    %extract text, splitting it by line
    data = textscan(fid,'%s','Delimiter','/');
    data = data{1};
    fclose(fid);

    %number of lines of text in the file
    file_length = length(data);
    
    num_inputs = 0;
    command_code_lists = {};
    arg_codes_lists = {};
    arg_types_lists = {};
    code_string_lists = {};
    for i = 1:file_length
        [command_code,arg_codes,arg_types] = parse_command_string(data{i}); 
        
        if command_code == 1
            num_inputs = num_inputs+1;
            command_code_lists{num_inputs} = [];
            arg_codes_lists{num_inputs} = [];
            arg_types_lists{num_inputs} = [];
            code_string_lists{num_inputs} = {};
        end

        command_code_lists{num_inputs}(end+1) = command_code;
        arg_codes_lists{num_inputs}(end+1,:) = arg_codes;
        arg_types_lists{num_inputs}(end+1,:) = arg_types;
        code_string_lists{num_inputs}{end+1} = data{i};
    end
    
    [p_list,q_list,div_list] = extract_key_info(arg_codes_lists)
    
    
%     for n = 1:10000
%         z_in = randi(5000);
%         digit_num = randi(14);
%         w_in = randi(9);
%         compare_functions(z_in,w_in,digit_num,...
%         command_code_lists,arg_codes_lists,arg_types_lists);
%     end

end

function compare_functions(z_in,w_in,digit_num,...
    command_code_lists,arg_codes_lists,arg_types_lists)

    [p_list,q_list,div_list] = extract_key_info(arg_codes_lists);

    z1 = verification_function(z_in,w_in,p_list(digit_num),q_list(digit_num),div_list(digit_num));
    z2 = run_codes_for_digit(z_in,w_in,command_code_lists{digit_num},arg_codes_lists{digit_num},arg_types_lists{digit_num});
    
    if z1~=z2
       disp('mismatch! uh oh!') 
    end
    
end

function [p_list,q_list,div_list] = extract_key_info(arg_codes_lists)
    p_list = [];
    q_list = [];
    div_list = [];
    
    for i = 1:length(arg_codes_lists)
        p_list(i) = arg_codes_lists{i}(6,2);
        q_list(i) = arg_codes_lists{i}(16,2);
        div_list(i) = arg_codes_lists{i}(5,2)==26;
    end
    
    p_list = p_list';
    q_list = q_list';
    div_list = div_list';
end


function z_out = verification_function(z_in,w_in,p,q,is_division)
    z_temp = z_in;
    if is_division
        z_temp = floor(z_in/26);
    end
    
    if mod(z_in,26)+p==w_in
        z_out = z_temp;
    else
        z_out = 26*z_temp + w_in +  q;
    end
end

function z_out = run_codes_for_digit...
    (z_in,w_in,command_codes,arg_codes,arg_types)

    current_register = [0,0,z_in,w_in];
    for i = 2:length(command_codes)
        current_register = run_command(current_register,command_codes(i),arg_codes(i,:),arg_types(i,:));
    end
    
    z_out = current_register(3);
end


function [z_list,w_list] = run_codes_for_digit_set...
    (command_code_lists,arg_codes_lists,arg_types_lists, z_start,input_range)

    num_digits = length(input_range);
    
    w_list = zeros(9^num_digits,num_digits);
    current_digits = ones(1,num_digits);
    count = 1;
    for i = 1:9^num_digits

        w_list(count,:)=current_digits;
        current_digits(end)=current_digits(end)+1;
        for j = num_digits:-1:2
           if current_digits(j)>9
               current_digits(j)=1;
               current_digits(j-1)=current_digits(j-1)+1;
           end
        end
        count = count+1;
    end
    z_list = [];
    
    for my_index=1:size(w_list,1)
        
        current_register = [0,0,z_start,0];
        for i = 1:num_digits
            current_register(4)=w_list(my_index,i);
            
            for j = 2:length(command_code_lists{input_range(i)})
                current_register = run_command(current_register,...
                    command_code_lists{input_range(i)}(j),...
                    arg_codes_lists{input_range(i)}(j,:),...
                    arg_types_lists{input_range(i)}(j,:));
            end
        end
%         current_register
        z_list(end+1)=current_register(3);
    end
%     z_list
end


function print_variable_importance(command_code_lists,arg_codes_lists,arg_types_lists)
    for register_num = 1:3
        variable_matters = 0;
        for i = 1:length(command_code_lists)
            if check_register_importance(command_code_lists{i}(2:end),...
                arg_codes_lists{i}(2:end,:),...
                arg_types_lists{i}(2:end,:),register_num)

                variable_matters = 1;
                break
            end
        end
        variable_char = char(register_num+'X'-1);
        if variable_matters
            disp([variable_char,' value from previous carries over'])
        else
            disp([variable_char,' value from previous does not carry over'])
        end
    end
end

function is_important = check_register_importance(command_code_list,arg_codes_list,arg_types_list,index_number)
    is_important = 0;
    for i = 1:length(command_code_list)
        if command_code_list(i)==3 ...
           && prod(arg_codes_list(i,:)==[index_number,0])==1 ...
           && prod(arg_types_list(i,:)==[1,0])==1
           
           break  
        end
        
        for j = 1:2
            if arg_types_list(i,j)==1 && arg_codes_list(i,j) == index_number
                is_important = 1;
                break
            end
        end
    end
end


function register_out = run_command(register_in,command_code,arg_codes,arg_types)
    arg_values = [0,0];
    for i = 1:2
        if arg_types(i)
            arg_values(i)=register_in(arg_codes(i));
        else
            arg_values(i)=arg_codes(i);
        end
    end
    
    a = arg_values(1);
    b = arg_values(2);
    
    store_result_register_index = arg_codes(1);
    my_answer = 0;
    
    if command_code == 2
        my_answer = a+b;
    end
        
    if command_code == 3
        my_answer = a*b;
    end
        
    if command_code == 4
        my_answer = floor(a/b);
    end
        
    if command_code == 5
        my_answer = mod(a,b);
    end
            
    if command_code == 6
        my_answer = a==b;
    end
    
    register_out = register_in;
    register_out(store_result_register_index) = my_answer;
    
end


function [command_code,arg_codes,arg_types] = parse_command_string(command_string) 
    command_str_list = strsplit(command_string,' ');

    num_args = 2;
    arg_codes = [0,0];
    arg_types = [0,0];
    
    if strcmp(command_str_list{1},'inp')
        command_code = 1;
        num_args = 1;
    end
    
    if strcmp(command_str_list{1},'add')
        command_code = 2;
    end
        
    if strcmp(command_str_list{1},'mul')
        command_code = 3;
    end
    
    if strcmp(command_str_list{1},'div')
        command_code = 4;
    end
    
    if strcmp(command_str_list{1},'mod')
        command_code = 5;
    end
    
    if strcmp(command_str_list{1},'eql')
        command_code = 6;
    end
    
    for i = 1:num_args
        is_symbolic_arg = 0;
        
        if strcmp(command_str_list{i+1},'x')
            arg_codes(i)=1;
            arg_types(i)=1;
            is_symbolic_arg = 1;
        end
                
        if strcmp(command_str_list{i+1},'y')
            arg_codes(i)=2;
            arg_types(i)=1;
            is_symbolic_arg = 1;
        end
                
        if strcmp(command_str_list{i+1},'z')
            arg_codes(i)=3;
            arg_types(i)=1;
            is_symbolic_arg = 1;
        end
                
        if strcmp(command_str_list{i+1},'w')
            arg_codes(i)=4;
            arg_types(i)=1;
            is_symbolic_arg = 1;
        end
        
        if ~is_symbolic_arg
            arg_codes(i)=str2num(command_str_list{i+1});
            arg_types(i)=0;
        end 
    end 
end





