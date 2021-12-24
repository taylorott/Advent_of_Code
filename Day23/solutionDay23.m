function solutionDay23()
format longG;

% 
% my_grid_string = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###.#.#.#.###'];...
%  ['  #.#.#.#.#  '];...
%  ['  #########  ']];


% state_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###B#C#B#D###'];...
%  ['  #A#D#C#A#  '];...
%  ['  #########  ']];
state_grid = ...
[['#############'];...
 ['#...........#'];...
 ['###D#A#C#A###'];...
 ['  #D#C#B#B#  '];...
 ['  #########  ']];


% state_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###C#B#A#D###'];...
%  ['  #A#B#C#D#  '];...
%  ['  #########  ']];


final_grid = ...
[['#############'];...
 ['#...........#'];...
 ['###A#B#C#D###'];...
 ['  #A#B#C#D#  '];...
 ['  #########  ']];

% state_grid = ...
% [['#############'];...
%  ['#AC.D.B.B.CC#'];...
%  ['###B#C#B#D###'];...
%  ['  #A#D#C#A#  '];...
%  ['  #########  ']];

% state_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###A#B#C#D###'];...
%  ['  #A#B#C#D#  '];...
%  ['  #########  ']];

% disp(state_grid);
%     
% state_code = grid_to_code(state_grid);
% disp(state_code);
% disp(code_to_grid(state_code));

% find_reachable_states(state_grid,1);

% [path_exists,man_distance] = check_path_room_to_hallway(state_grid,[3,4],[2,2])
% [path_exists,man_distance] = check_path_hallway_to_room(state_grid,[2,2],[3,4])

% myTable = OrionHashTable(1000);
% myTable.insert(12342,50);
% myTable.get_value(12342)
% myTable.contains_key(5)
% myTable.contains_key(12342)

start_code = grid_to_code(state_grid);
final_code = grid_to_code(final_grid);

table_size = 20000;
myQueue = OrionPriorityQueue(table_size);
myQueue.push(start_code,0);
final_set_table = OrionHashTable(table_size);
reverse_map = OrionHashTable(table_size);
tic
while myQueue.num_elements>0
    [current_state_code,cost_to_go] =  myQueue.pop();
    final_set_table.insert(current_state_code,cost_to_go);
    
    if current_state_code == final_code
        break;
    end
    
    
    [reachable_state_codes,reachable_cost_vec] = find_reachable_states(code_to_grid(current_state_code),0);
    

    for i=1:length(reachable_state_codes)
        code_to_update = reachable_state_codes(i);
        current_incremental_cost = reachable_cost_vec(i);
        if final_set_table.contains_key(code_to_update)~=1
            if myQueue.priority_queue_index_map.contains_key(code_to_update)==0
                myQueue.push(code_to_update,cost_to_go+current_incremental_cost);
                reverse_map.insert(code_to_update,current_state_code);
            else
                old_cost_to_go = myQueue.get_key_value(code_to_update);
                if cost_to_go+current_incremental_cost<old_cost_to_go
                    myQueue.decrement_key(code_to_update,cost_to_go+current_incremental_cost);
                    reverse_map.update_value(code_to_update,current_state_code);
                end
            end
            
        end
%         if final_set_matrix(update_index)~=1
%             cost_to_go(update_index)=min(my_mat(update_index)+cost_to_go(my_index),cost_to_go(update_index));
%             if neighbor_set_matrix(update_index)==0
%                 neighbor_set_matrix(update_index)=1;
%                 push(update_index)
%             else
%                 sift_up(priority_queue_index_list(update_index));
%             end
%         end
    end
end

% 
final_code_sequence = [final_code];
next_code = -1;
while next_code~=start_code
    next_code = reverse_map.get_value(final_code_sequence(end));
    final_code_sequence(end+1) = next_code;
end
final_code_sequence = final_code_sequence(end:-1:1);

for i = final_code_sequence  
    disp(code_to_grid(i));
    disp(' ');
end

final_set_table.get_value(grid_to_code(final_grid))
toc
end


function [state_codes,cost_vec] = find_reachable_states(current_grid,display_boolean)
    state_codes = [];
    cost_vec = [];
    blank_vec = [' ';' ';' ';' ';' '];
    move_cost = [1,10,100,1000];
    hallway_indices = [[2,2];[2,3];[2,5];[2,7];[2,9];[2,11];[2,12]];
    num_hallway_spots = size(hallway_indices,1);

    room_indices = {};
    room_indices{1} = [[3,4];[4,4]];
    room_indices{2} = [[3,6];[4,6]];
    room_indices{3} = [[3,8];[4,8]];
    room_indices{4} = [[3,10];[4,10]];

    %check for moves that put amphipods into hallway spots
    for amphipod_type = 1:4
        start_coord = [];
        move_can_happen = 0;
        %if the front portion of the room is occupied
        if current_grid(room_indices{amphipod_type}(1,1),room_indices{amphipod_type}(1,2))~='.'
            %the amphipod will need to move out of the way if it is not in
            %the correct room, or its back roommate is not in the correct room
            if (current_grid(room_indices{amphipod_type}(1,1),room_indices{amphipod_type}(1,2))-'A'+1 ~=amphipod_type)...
             ||(current_grid(room_indices{amphipod_type}(2,1),room_indices{amphipod_type}(2,2))-'A'+1 ~=amphipod_type)
         
                start_coord = room_indices{amphipod_type}(1,:);
                move_can_happen = 1;
            end
        else
            %if the back portion of the room if occupied but not the front portion
            %and this back portion of the room has an amphipod of the wrong type
            if current_grid(room_indices{amphipod_type}(2,1),room_indices{amphipod_type}(2,2))~='.' ...
               &&(current_grid(room_indices{amphipod_type}(2,1),room_indices{amphipod_type}(2,2))-'A'+1 ~=amphipod_type)
           
                start_coord = room_indices{amphipod_type}(2,:);
                move_can_happen = 1;   
            end
        end
        
        if move_can_happen==1
            for i = 1:num_hallway_spots
                end_coord = hallway_indices(i,:);
                [path_exists,man_distance] = check_path_room_to_hallway(current_grid,start_coord,end_coord);
                if path_exists
                    moving_amphipod_type = current_grid(start_coord(1),start_coord(2))-'A'+1;
                    new_grid_string = current_grid;
                    new_grid_string(end_coord(1),end_coord(2))=current_grid(start_coord(1),start_coord(2));
                    new_grid_string(start_coord(1),start_coord(2)) = '.';
                    if display_boolean==1
                        disp([current_grid,blank_vec,new_grid_string]);
                        disp(' ');
                    end
                    state_codes(end+1)=grid_to_code(new_grid_string);
                    cost_vec(end+1)=man_distance*move_cost(moving_amphipod_type);
                end
            end
        end
    end
    
    %check for moves that put amphipods back in the correct room
    %from the hallway
    for i = 1:num_hallway_spots
        %if amphipod seen in hallway
        if current_grid(hallway_indices(i,1),hallway_indices(i,2))~='.'
            %figure out which room it needs to go into
            amphipod_type = current_grid(hallway_indices(i,1),hallway_indices(i,2))-'A'+1;
            
            %starting position of that amphipod
            start_coord = hallway_indices(i,:);
            
            %if the back space of the correct room is empty, we can move in
            %note that we will never have a situation where of room back is empty
            %but not the front of the room, since we move to back of room first
            if current_grid(room_indices{amphipod_type}(2,1),room_indices{amphipod_type}(2,2))=='.'
                
                end_coord = room_indices{amphipod_type}(2,:);
                [path_exists,man_distance] = check_path_hallway_to_room(current_grid,start_coord,end_coord);
                if path_exists
                    new_grid_string = current_grid;
                    new_grid_string(end_coord(1),end_coord(2))=current_grid(start_coord(1),start_coord(2));
                    new_grid_string(start_coord(1),start_coord(2)) = '.';
                    if display_boolean==1
                        disp([current_grid,blank_vec,new_grid_string]);
                        disp(' ');
                    end
                    state_codes(end+1)=grid_to_code(new_grid_string);
                    cost_vec(end+1)=man_distance*move_cost(amphipod_type);
                end
                
            else
                %otherwise, if the back of the room contains the correct
                %type of amphipod, and the front of the room is empty
                %we can move into the front of the room
                if (current_grid(room_indices{amphipod_type}(2,1),room_indices{amphipod_type}(2,2))-'A'+1) == amphipod_type...
                  && current_grid(room_indices{amphipod_type}(1,1),room_indices{amphipod_type}(1,2))=='.'
              
                    end_coord = room_indices{amphipod_type}(1,:);
                    [path_exists,man_distance] = check_path_hallway_to_room(current_grid,start_coord,end_coord);
                    if path_exists
                        new_grid_string = current_grid;
                        new_grid_string(end_coord(1),end_coord(2))=current_grid(start_coord(1),start_coord(2));
                        new_grid_string(start_coord(1),start_coord(2)) = '.';
                        if display_boolean==1
                            disp([current_grid,blank_vec,new_grid_string]);
                            disp(' ');
                        end
                        state_codes(end+1)=grid_to_code(new_grid_string);
                        cost_vec(end+1)=man_distance*move_cost(amphipod_type);
                    end
                end
            end
        end
    end
    
end

function [path_exists,man_distance] = check_path_room_to_hallway(grid_string,start_coord,end_coord)
    path_exists = 1;
    man_distance =sum(abs(end_coord-start_coord));
    while path_exists==1 && (start_coord(1)~=end_coord(1) || start_coord(2)~=end_coord(2))
        my_delta = [0,0];
        if start_coord(1)~=end_coord(1)
            my_delta = [-1,0];
        else
            my_delta = [0,sign(end_coord(2)-start_coord(2))];
        end
        
        start_coord = start_coord + my_delta;
        if grid_string(start_coord(1),start_coord(2))~='.'
            path_exists = 0;
        end
    end
end

function [path_exists,man_distance] = check_path_hallway_to_room(grid_string,start_coord,end_coord)
    path_exists = 1;
    man_distance =sum(abs(end_coord-start_coord));
    while path_exists==1 && (start_coord(1)~=end_coord(1) || start_coord(2)~=end_coord(2))
        my_delta = [0,0];
        if start_coord(2)~=end_coord(2)
            my_delta = [0,sign(end_coord(2)-start_coord(2))];
        else
            my_delta = [1,0];
        end
        
        start_coord = start_coord + my_delta;
        if grid_string(start_coord(1),start_coord(2))~='.'
            path_exists = 0;
        end
    end 
end


function state_code = grid_to_code(grid_string)
    state_code =...
                vector_to_code(...
                string_to_vector(...
                grid_to_string(...
                grid_string)));
end

function grid_string = code_to_grid(state_code)
    grid_string =   ...
                    string_to_grid(...
                    vector_to_string(...
                    code_to_vector(...
                    state_code)));
               
end

function state_code = vector_to_code(state_vector)
    state_code = sum((5.^(0:14)).*state_vector);
end

function state_vector = code_to_vector(state_code)
    state_vector = zeros(1,15);
    for i = 1:15
        state_vector(i)=rem(state_code,5);
        state_code = (state_code-state_vector(i))/5;
    end
end

function state_string = vector_to_string(state_vector) 
    state_string = char(...
                   46*(state_vector==0)...
                  +65*(state_vector==1)...
                  +66*(state_vector==2)...
                  +67*(state_vector==3)...
                  +68*(state_vector==4));
end

function state_vector = string_to_vector(state_string)
    state_vector = 0*(state_string=='.')...
                  +1*(state_string=='A')...
                  +2*(state_string=='B')...
                  +3*(state_string=='C')...
                  +4*(state_string=='D');
end

function grid_string = string_to_grid(state_string)
    grid_string = ...
    [['#############'];...
     ['#...........#'];...
     ['###.#.#.#.###'];...
     ['  #.#.#.#.#  '];...
     ['  #########  ']];

    grid_string(2,2:3)=state_string(1:2);
    grid_string(2,5)=state_string(3);
    grid_string(2,7)=state_string(4);
    grid_string(2,9)=state_string(5);
    grid_string(2,11:12)=state_string(6:7);
    grid_string(3,4)=state_string(8);
    grid_string(3,6)=state_string(9);
    grid_string(3,8)=state_string(10);
    grid_string(3,10)=state_string(11);
    grid_string(4,4)=state_string(12);
    grid_string(4,6)=state_string(13);
    grid_string(4,8)=state_string(14);
    grid_string(4,10)=state_string(15);
end

function state_string = grid_to_string(grid_string)
    state_string(1:15)='.';
    
    state_string(1:2)=grid_string(2,2:3);
    state_string(3)  =grid_string(2,5);
    state_string(4)  =grid_string(2,7);
    state_string(5)  =grid_string(2,9);
    state_string(6:7)=grid_string(2,11:12);
    state_string(8)  =grid_string(3,4);
    state_string(9)  =grid_string(3,6);
    state_string(10) =grid_string(3,8);
    state_string(11) =grid_string(3,10);
    state_string(12) =grid_string(4,4);
    state_string(13) =grid_string(4,6);
    state_string(14) =grid_string(4,8);
    state_string(15) =grid_string(4,10);
end





