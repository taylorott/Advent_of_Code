function solutionDay23()
format longG;

% digits(50);
% 
% my_grid_string = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###.#.#.#.###'];...
%  ['  #.#.#.#.#  '];...
%  ['  #########  ']];
% 
% state_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###D#A#C#A###'];...
%  ['  #D#C#B#B#  '];...
%  ['  #########  ']];

% state_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###B#C#B#D###'];...
%  ['  #A#D#C#A#  '];...
%  ['  #########  ']];

% state_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###B#C#B#D###'];...
%  ['  #D#C#B#A#  '];...
%  ['  #D#B#A#C#  '];...
%  ['  #A#D#C#A#  '];...
%  ['  #########  ']];


% state_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###C#B#A#D###'];...
%  ['  #A#B#C#D#  '];...
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
 ['  #D#C#B#A#  '];...
 ['  #D#B#A#C#  '];...
 ['  #D#C#B#B#  '];...
 ['  #########  ']];

final_grid = ...
[['#############'];...
 ['#...........#'];...
 ['###A#B#C#D###'];...
 ['  #A#B#C#D#  '];...
 ['  #A#B#C#D#  '];...
 ['  #A#B#C#D#  '];...
 ['  #########  ']];

% final_grid = ...
% [['#############'];...
%  ['#...........#'];...
%  ['###A#B#C#D###'];...
%  ['  #A#B#C#D#  '];...
%  ['  #########  ']];

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

global room_depth;
room_depth = 4;
% room_depth = 2;
initialize_values();

start_vector = grid_to_vector(state_grid);
final_vector = grid_to_vector(final_grid);

% code_to_grid(start_code);
% code_to_grid(final_code)
% find_reachable_states(code_to_grid(start_code),1);

table_size = 20000;
myQueue = OrionPriorityQueue(table_size);
myQueue.push(start_vector,0);
final_set_table = OrionHashTable(table_size);
reverse_map = OrionHashTable(table_size);

% count = 1;
tic
while myQueue.num_elements>0
%     count = count+1
%     is_valid1 = myQueue.test_table_validity();
    [current_state_vector,cost_to_go] =  myQueue.pop();
%     is_valid2 = myQueue.test_table_validity();

%     if is_valid1==1 && is_valid2==0
%         'uh oh! pop is bad'
%     end
                
%     cost_to_go
    final_set_table.insert(current_state_vector,cost_to_go);
%     current_state_vector
%     cost_to_go
%     final_set_table.get_value(current_state_vector)
    
    if prod(current_state_vector == final_vector)==1
%         'hello!'
        break;
    end
    
    
    [reachable_state_vectors,reachable_cost_vec] = find_reachable_states(current_state_vector,0);
    
%     reachable_state_vectors
    for i=1:size(reachable_state_vectors,1)
        vector_to_update = reachable_state_vectors(i,:);
        current_incremental_cost = reachable_cost_vec(i);
        if final_set_table.contains_key(vector_to_update)~=1
            if myQueue.priority_queue_index_map.contains_key(vector_to_update)==0
%                 is_valid1 = myQueue.test_table_validity();
                myQueue.push(vector_to_update,cost_to_go+current_incremental_cost);
%                 is_valid2 = myQueue.test_table_validity();
                
%                 if is_valid1==1 && is_valid2==0
%                     'uh oh! push is bad'
%                 end
                reverse_map.insert(vector_to_update,current_state_vector);
                
                old_cost_to_go = myQueue.get_key_value(vector_to_update);
                temp_value_array = myQueue.priority_queue_index_map.get_value(vector_to_update);
                if prod(myQueue.my_key_queue{temp_value_array(1)}==vector_to_update)==0 
                    [myQueue.my_key_queue{temp_value_array(1)};vector_to_update]
                    [myQueue.my_value_queue(temp_value_array(1)),old_cost_to_go,cost_to_go+current_incremental_cost]
                end
            else
                old_cost_to_go = myQueue.get_key_value(vector_to_update);
                temp_value_array = myQueue.priority_queue_index_map.get_value(vector_to_update);
                if prod(myQueue.my_key_queue{temp_value_array(1)}==vector_to_update)==0 
                    [myQueue.my_key_queue{temp_value_array(1)};vector_to_update]
                    [myQueue.my_value_queue(temp_value_array(1)),old_cost_to_go]
                end
                if cost_to_go+current_incremental_cost<old_cost_to_go
                    myQueue.decrement_key(vector_to_update,cost_to_go+current_incremental_cost);
                    reverse_map.update_value(vector_to_update,current_state_vector);
                end
            end
            
        end
    end
end


final_vector_sequence = [final_vector];
next_vector = -1;
while prod(next_vector==start_vector)~=1
%     disp(vector_to_grid(final_vector_sequence(end,:)));
%     disp(' ');
    
    next_vector = reverse_map.get_value(final_vector_sequence(end,:));
    final_vector_sequence(end+1,:) = next_vector;
end
final_vector_sequence = final_vector_sequence(end:-1:1,:);

for i = 1:size(final_vector_sequence,1)  
    disp(vector_to_grid(final_vector_sequence(i,:)));
    disp(final_set_table.get_value(final_vector_sequence(i,:)))
    disp(' ');
end

final_set_table.get_value(final_vector)
toc
end

function initialize_values()
    global room_depth;
    global hallway_indices;
    global num_hallway_spots;
    global move_cost;
    global room_indices;
    global room_x_coords;
    global hallway_x_coords;
    global blank_vec;
    blank_vec = [];
    room_x_coords = [4,6,8,10];
    
    
    move_cost = [1,10,100,1000];
    hallway_indices = [[2,2];[2,3];[2,5];[2,7];[2,9];[2,11];[2,12]];
    hallway_x_coords = hallway_indices(:,2)';
    num_hallway_spots = size(hallway_indices,1);
    room_indices = {};
    
    blank_vec(1:(room_depth+3),1)=' ';
    for i = 1:4
        room_indices{i}=[(3:(3+room_depth-1))',(2*i+2)*ones(room_depth,1)];
    end
end


function [state_vectors,cost_vec] = find_reachable_states(input_vector,display_boolean)
    global room_depth;
    global hallway_indices;
    global num_hallway_spots;
    global move_cost;
    global room_indices;
    global blank_vec;

    current_grid = vector_to_grid(input_vector);
    state_vectors = [];
    cost_vec = [];

    correct_placement_from_room = 0;
    correct_placement_from_hallway = 0;
    
    
    %the amount of amphipods in each room that need to leave at some point
    junk_on_top = zeros(1,4);
    open_spots_on_top = zeros(1,4);
  
    for i = 1:4
        good_so_far = 1;
        for j = room_depth:-1:1
            if current_grid(room_indices{i}(j,1),room_indices{i}(j,2))=='.'
                open_spots_on_top(i) = open_spots_on_top(i)+1;
            else 
                if current_grid(room_indices{i}(j,1),room_indices{i}(j,2))-'A'+1~=i
                    good_so_far = 0;
                    
                end

                if good_so_far~=1
                    junk_on_top(i)=junk_on_top(i)+1;
                end
            end
        end
    end
    first_nonempty_index_list = open_spots_on_top+1;
    room_is_clear = junk_on_top==0;
    

    
    
    %check for moves that put amphipods directly into good rooms
    for room_number = 1:4
        move_can_happen = 0;
        
        first_nonempty_index = first_nonempty_index_list(room_number);
        
        
        if room_is_clear(room_number)==0
            start_coord = room_indices{room_number}(first_nonempty_index,:);
            moving_amphipod_type = current_grid(start_coord(1),start_coord(2))-'A'+1;

            if room_is_clear(moving_amphipod_type)==1
                end_coord = room_indices{moving_amphipod_type}(open_spots_on_top(moving_amphipod_type),:);
                

                path_exists = prod(current_grid(2,min(start_coord(2),end_coord(2)):max(start_coord(2),end_coord(2)))=='.')==1;
                man_distance = abs(start_coord(2)-end_coord(2))+open_spots_on_top(room_number)+open_spots_on_top(moving_amphipod_type)+1;
%                 current_grid
                if path_exists
                    correct_placement_from_room = 1;
                    
                    new_grid_string = current_grid;
                    new_grid_string(end_coord(1),end_coord(2))=current_grid(start_coord(1),start_coord(2));
                    new_grid_string(start_coord(1),start_coord(2)) = '.';
                    if display_boolean==1
                        disp(['can move amphipod directly from start to final rooms'])
                        disp(['start room number: ', num2str(room_number), ' destination room: ',num2str(moving_amphipod_type)]);
                        disp([current_grid,blank_vec,new_grid_string]);
                        disp(' ');
                    end
                    state_vectors(end+1,:)=grid_to_vector(new_grid_string);
                    cost_vec(end+1)=man_distance*move_cost(moving_amphipod_type);
                    break;
                end    
            end
        end
    end
    
    
    if correct_placement_from_room~=1
        %check for moves that put amphipods back in the correct room
        %from the hallway
        for i = 1:num_hallway_spots
            %if amphipod seen in hallway
            if current_grid(hallway_indices(i,1),hallway_indices(i,2))~='.'
                %figure out which room it needs to go into
                moving_amphipod_type = current_grid(hallway_indices(i,1),hallway_indices(i,2))-'A'+1;

                %starting position of that amphipod
                start_coord = hallway_indices(i,:);
                
                if room_is_clear(moving_amphipod_type)==1
                    end_coord = room_indices{moving_amphipod_type}(open_spots_on_top(moving_amphipod_type),:);
                    [path_exists,man_distance] = check_path_hallway_to_room(current_grid,start_coord,end_coord);
                    if path_exists
                        correct_placement_from_hallway = 1;
                        new_grid_string = current_grid;
                        new_grid_string(end_coord(1),end_coord(2))=current_grid(start_coord(1),start_coord(2));
                        new_grid_string(start_coord(1),start_coord(2)) = '.';
                        if display_boolean==1
                            disp('can place directly from hallway')
                            disp(['hallway index: ',num2str(i),' room number: ',num2str(moving_amphipod_type)])
                            disp([current_grid,blank_vec,new_grid_string]);
                            disp(' ');
                        end
                        state_vectors(end+1,:)=grid_to_vector(new_grid_string);
                        cost_vec(end+1)=man_distance*move_cost(moving_amphipod_type);
                        break;
                    end
                end
            end
        end
    
    end
    
    if correct_placement_from_room~=1 && correct_placement_from_hallway~=1
        %check for moves that put amphipods into hallway spots
        for room_number = 1:4
            move_can_happen = 0;

            %first index of room to not be '.', value is 5 if room is empty
            first_nonempty_index = first_nonempty_index_list(room_number);

            if room_is_clear(room_number)==0
                start_coord = room_indices{room_number}(first_nonempty_index,:);
            
                for i = 1:num_hallway_spots
                    end_coord = hallway_indices(i,:);
                    [path_exists,man_distance] = check_path_room_to_hallway(current_grid,start_coord,end_coord);
                    if path_exists
                        moving_amphipod_type = current_grid(start_coord(1),start_coord(2))-'A'+1;
                        
                        is_useful = check_rth_move_usefuleness(current_grid,room_number,first_nonempty_index,i);
                        
                        if is_useful==1
%                             disp('is useful')
                            new_grid_string = current_grid;
                            new_grid_string(end_coord(1),end_coord(2))=current_grid(start_coord(1),start_coord(2));
                            new_grid_string(start_coord(1),start_coord(2)) = '.';
%                             if display_boolean==1
%                                 disp([current_grid,blank_vec,new_grid_string]);
%                                 disp(' ');
%                             end
                            state_vectors(end+1,:)=grid_to_vector(new_grid_string);
                            cost_vec(end+1)=man_distance*move_cost(moving_amphipod_type);
                        end
                    end
                end
            end
        end
    end
end

function is_useful = check_rth_move_usefuleness(grid_string,start_room,start_depth,hallway_index)
    is_useful = 0;
    
    global room_depth;
    global hallway_indices;
    global num_hallway_spots;
    global room_indices;
    global blank_vec;
    global room_x_coords;
    
    start_coord = room_indices{start_room}(start_depth,:);
    start_char = grid_string(start_coord(1),start_coord(2));
    target_room_start_char = start_char-'A'+1;
    end_coord = hallway_indices(hallway_index,:);
    
    new_grid = grid_string;
    new_grid(end_coord(1),end_coord(2))=start_char;
    new_grid(start_coord(1),start_coord(2))='.';
    
  
    
    %the amount of amphipods in each room that need to leave at some point
    junk_on_top = zeros(1,4);
    open_spots_on_top = zeros(1,4);
    room_is_clear = ones(1,4);
    for i = 1:4
        good_so_far = 1;
        for j = room_depth:-1:1
            if grid_string(room_indices{i}(j,1),room_indices{i}(j,2))=='.'
                open_spots_on_top(i) = open_spots_on_top(i)+1;
            else 
                if grid_string(room_indices{i}(j,1),room_indices{i}(j,2))-'A'+1~=i
                    good_so_far = 0;
                    room_is_clear(i)=0;
                end

                if good_so_far~=1
                    junk_on_top(i)=junk_on_top(i)+1;
                end
            end
        end
    end
    
%     deadlock_detected = 0;
    deadlock_count = 0;
    for i = (open_spots_on_top(target_room_start_char)+1):room_depth
        start_x_needs_moved = room_x_coords(target_room_start_char);
        need_moved_char = grid_string(room_indices{target_room_start_char}(i,1),room_indices{target_room_start_char}(i,2));
        needs_moved_char_room = grid_string(room_indices{target_room_start_char}(i,1),room_indices{target_room_start_char}(i,2))-'A'+1;
        end_x_needs_moved =  room_x_coords(needs_moved_char_room);
        minX_deadlock = min(start_x_needs_moved,end_x_needs_moved);
        maxX_deadlock = max(start_x_needs_moved,end_x_needs_moved);
        if minX_deadlock<=end_coord(2) && end_coord(2) <= maxX_deadlock
            deadlock_count = deadlock_count+1;
%             deadlock_detected = 1;
%             disp(['deadlock detected. cannot move'])
%             disp(['Starting room: ',num2str(start_room),' hallway spot: ',num2str(hallway_index)])
%             disp(['blocks the: ',need_moved_char,' at depth ',num2str(i),' in room ',num2str(target_room_start_char) ])
%             disp([grid_string,blank_vec,new_grid]);
%             disp(' ');
%             break
        end
    end
    
    deadlock_detected = deadlock_count>=3;
    if deadlock_detected==0
        
        if is_useful~=1
            total_shit_to_move = junk_on_top(start_room);
            for i = 1:num_hallway_spots
                clear_character = grid_string(hallway_indices(i,1),hallway_indices(i,2));
                if clear_character-'A'+1==start_room
                    
                    [available_spots,transfer_possible] = find_available_hallways_spots_hallway_transfer(new_grid,start_room,i);
    %              	disp(['Move from room ',num2str(start_room),' to completely clear'])
    %                 disp(['for ' clear_character,' in hallway index ',num2str(i)]);
    %                 disp(['Remaining shit to move = ',num2str(total_shit_to_move-1),' spots to put em ', num2str(available_spots)]);
    %                 disp(['junk remaining in target room: ',num2str(junk_on_top(start_room)-1)]);
    %                 disp([grid_string,blank_vec,new_grid]);
    %                 disp(' ');
                     if transfer_possible==1 && available_spots>=(total_shit_to_move-1)
                        is_useful=1;
%                         disp(['Move from room ',num2str(start_room),' to completely clear'])
%                         disp(['for ' clear_character,' in hallway index ',num2str(i)]);
%                         disp(['Remaining shit to move = ',num2str(total_shit_to_move-1),' spots to put em ', num2str(available_spots)]);
%                         disp(['junk remaining in target room: ',num2str(junk_on_top(start_room)-1)]);

                        break;
                     end     
                end
            end
        end


        %check the stuff that is trapped to see if it's worth moving
        for i = 1:(junk_on_top(start_room)-1)
            target_index = start_depth+i;
            target_room = grid_string(room_indices{start_room}(target_index,1),room_indices{start_room}(target_index,2))-'A'+1;
            clear_character = grid_string(room_indices{start_room}(target_index,1),room_indices{start_room}(target_index,2));
            total_shit_to_move = i+junk_on_top(target_room);

            [available_spots,transfer_possible] = find_available_hallways_spots_room_transfer(new_grid,start_room,target_room);
            if transfer_possible==1 && available_spots>=(total_shit_to_move-1)
                is_useful=1;
%                 disp(['Move from room ',num2str(start_room),' to free ', clear_character,' at depth ', num2str(target_index)]);
%                 disp(['Remaining shit to move = ',num2str(total_shit_to_move-1),' spots to put em ', num2str(available_spots)]);
%                 disp(['target room ', num2str(target_room),' junk in target room: ',num2str(junk_on_top(target_room))]);

                break;
            end
        end

        if is_useful~=1    
            for target_room = 1:4
                if target_room~=start_room
                   for target_depth= (open_spots_on_top(target_room)+1):room_depth
                       if grid_string(room_indices{target_room}(target_depth,1),room_indices{target_room}(target_depth,2))-'A'+1==start_room
                           clear_character = grid_string(room_indices{target_room}(target_depth,1),room_indices{target_room}(target_depth,2));
                           total_shit_to_move = junk_on_top(start_room) + target_depth-open_spots_on_top(target_room)-1;

                           [available_spots,transfer_possible] = find_available_hallways_spots_room_transfer(new_grid,start_room,target_room);
                           if transfer_possible==1 && available_spots>=(total_shit_to_move-1)
                                is_useful=1;
%                                 disp(['Move from room ',num2str(start_room),' to completely clear'])
%                                 disp(['for ' clear_character,' in room ',num2str(target_room),' and depth', num2str(target_depth)]);
%                                 disp(['Remaining shit to move = ',num2str(total_shit_to_move-1),' spots to put em ', num2str(available_spots)]);
%                                 disp(['junk remaining in target room: ',num2str(junk_on_top(target_room)-1)]);
                                break;
                           end

                       end
                   end
                end
            end
        end

    end

    is_useful = ~deadlock_detected;
end

function [available_spots,transfer_possible] = find_available_hallways_spots_hallway_transfer(grid_string,roomA,hallwayB)
    global room_x_coords;
    global hallway_x_coords;

    
    hallway_x = hallway_x_coords(hallwayB);
    room_x = room_x_coords(roomA);
    hallway_x = hallway_x+sign(room_x-hallway_x);
    minX = min(hallway_x,room_x);
    maxX = max(hallway_x,room_x);
%     [minX,maxX]
%     grid_string(2,minX:maxX)~='.'
    transfer_possible = sum(grid_string(2,minX:maxX)~='.')==0;
  
    available_spots = 0;
    if transfer_possible == 1
        current_index = minX;
        while current_index>1 && grid_string(2,current_index)=='.'
            if mod(current_index,2)==1 || current_index==2 
               available_spots = available_spots+1; 
            end
            current_index = current_index-1;
            
        end
        
        current_index = maxX;
        while current_index<13 && grid_string(2,current_index)=='.'
            if mod(current_index,2)==1 || current_index==12
               available_spots = available_spots+1; 
            end
            current_index = current_index+1;
        end
    end
end



function [available_spots,transfer_possible] = find_available_hallways_spots_room_transfer(grid_string,roomA,roomB)
    global room_x_coords;
    transfer_possible = sum(grid_string(2,room_x_coords(min(roomA,roomB)):room_x_coords(max(roomA,roomB)))~='.')==0;
  
    available_spots = 0;
    if transfer_possible == 1
        current_index = room_x_coords(min(roomA,roomB));
        while current_index>1 && grid_string(2,current_index)=='.'
            if mod(current_index,2)==1 || current_index==2 
               available_spots = available_spots+1; 
            end
            current_index = current_index-1;
            
        end
        
        current_index = room_x_coords(max(roomA,roomB));
        while current_index<13 && grid_string(2,current_index)=='.'
            if mod(current_index,2)==1 || current_index==12
               available_spots = available_spots+1; 
            end
            current_index = current_index+1;
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

function state_vector = grid_to_vector(grid_string)
    state_vector =...
                string_to_vector(...
                grid_to_string(...
                grid_string));
end

function grid_string = vector_to_grid(state_vector)
    grid_string =   ...
                    string_to_grid(...
                    vector_to_string(...
                    state_vector));         
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

function state_code = vector_to_code(state_vector)
    global room_depth;
    
    if room_depth==2
        state_code = vector_to_code_depth2(state_vector);
    end
    
    if room_depth==4
        state_code = vector_to_code_depth4(state_vector);
    end
end

function state_vector = code_to_vector(state_code)
    global room_depth;
    
    if room_depth==2
        state_vector = code_to_vector_depth2(state_code);
    end
    
    if room_depth==4
        state_vector = code_to_vector_depth4(state_code);
    end
end

function grid_string = string_to_grid(state_string)
    global room_depth;
    
    if room_depth==2
        grid_string = string_to_grid_depth2(state_string);
    end
    
    if room_depth==4
        grid_string = string_to_grid_depth4(state_string);
    end
end

function state_string = grid_to_string(grid_string)
    global room_depth;
    
    if room_depth==2
        state_string = grid_to_string_depth2(grid_string);
    end
    
    if room_depth==4
        state_string = grid_to_string_depth4(grid_string);
    end
end

function state_code = vector_to_code_depth4(state_vector)
    state_code = sum((5.^(0:22)).*state_vector);
end

function state_vector = code_to_vector_depth4(state_code)
    state_vector = zeros(1,23);
    for i = 1:23
        state_vector(i)=rem(state_code,5);
        state_code = (state_code-state_vector(i))/5;
    end
end


function grid_string = string_to_grid_depth4(state_string)
    grid_string = ...
    [['#############'];...
     ['#...........#'];...
     ['###.#.#.#.###'];...
     ['###.#.#.#.###'];...
     ['###.#.#.#.###'];...
     ['###.#.#.#.###'];...
     ['#############']];

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
    grid_string(5,4)=state_string(16);
    grid_string(5,6)=state_string(17);
    grid_string(5,8)=state_string(18);
    grid_string(5,10)=state_string(19);
    grid_string(6,4)=state_string(20);
    grid_string(6,6)=state_string(21);
    grid_string(6,8)=state_string(22);
    grid_string(6,10)=state_string(23);
end

function state_string = grid_to_string_depth4(grid_string)
    state_string(1:23)='.';
    
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
    state_string(16) =grid_string(5,4);
    state_string(17) =grid_string(5,6);
    state_string(18) =grid_string(5,8);
    state_string(19) =grid_string(5,10);
    state_string(20) =grid_string(6,4);
    state_string(21) =grid_string(6,6);
    state_string(22) =grid_string(6,8);
    state_string(23) =grid_string(6,10);
end

function state_code = vector_to_code_depth2(state_vector)
    state_code = sum((5.^(0:14)).*state_vector);
end

function state_vector = code_to_vector_depth2(state_code)
    state_vector = zeros(1,15);
    for i = 1:15
        state_vector(i)=rem(state_code,5);
        state_code = (state_code-state_vector(i))/5;
    end
end


function grid_string = string_to_grid_depth2(state_string)
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

function state_string = grid_to_string_depth2(grid_string)
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





