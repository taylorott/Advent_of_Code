function solutionDay19a()
    tic
    
    %parse the input file
    [parsed_beacon_data,num_scanners]=parse_data_file();
    
    %build the squared distance matrix for each scanner from the beacon coordinates
    [dmat_list,dsignature_list,dsignature_index_list] = build_all_distance_information(parsed_beacon_data,num_scanners);
    
    %build a graph connecting all of the scanners given the information
    %collected so far
    [my_graph_forward_transformation_list,my_graph_indices_list] = build_Graph(parsed_beacon_data,dmat_list,dsignature_list,dsignature_index_list);
    
    %using the graph that connects all the scanners, find the rigid body
    %transformations connecting each scanner frame to the scanner 0 frame
    scanner_forward_transformations = compute_frame0_transformations(my_graph_forward_transformation_list,my_graph_indices_list);
    
    %time to convert every beacon seen by each of the scanners into
    %the scanner 0 frame
    
    %matrix of beacon coords in the scanner 0 frame
    scanner0_beacon_coords = [];
    
    %iterate through each scanner
    for i = 1:num_scanners
        %map the beacon coordinates of the scanner_index'th scanner
        %into the scanner 0 frame, and append to the total list of beacon coords
        scanner0_beacon_coords = [scanner0_beacon_coords,transform_coords(parsed_beacon_data{i},scanner_forward_transformations{i})];
    end
    
    %compute and print the number of unique beacons that we see
    compute_num_unique_beacons(scanner0_beacon_coords);
    
    %now we compile a list of the position of each of the scanners in the
    %scanner 0 frame
    
    %matrix of scanner coords in the scanner 0 frame
    scanner_coord_matrix = zeros(3,num_scanners);
    
    %iterate through each scanner
    for i = 1:num_scanners
        %and extract the scanner 0 frame coordinates of that scanner
        %from the rigid body transformation matrix
        scanner_coord_matrix(:,i)=scanner_forward_transformations{i}(1:3,4);
    end
    
    %finally, compute the max manhattan distance between all scanner
    %positions, and then print out the result
    compute_max_manhattan_distance(scanner_coord_matrix)

    toc
end

%this function takes the graph that we have constructed that connects the
%frames of each of the scanner frames, and constructs the list of 
function [scanner_forward_transformations] = compute_frame0_transformations(my_graph_forward_transformation_list,my_graph_indices_list)
    num_scanners = length(my_graph_indices_list);

    %this is the list of scanners that we currently know that scanner 0
    %rigid body transformation for
    scanner_indices = my_graph_indices_list{1};
    
    %scanner_forward_transformations{i} is the 
    %rigid body transformation mapping a coordinate in
    %the scanner i frame to the scanner 0 frame
    scanner_forward_transformations = cell(num_scanners,1);
    
    %initialize scanner_forward_transformations with the transformations
    %that we already have
    for i = 1:length(scanner_indices)
        scanner_forward_transformations{scanner_indices(i)} = my_graph_forward_transformation_list{1}{i};
    end

    %iterate through the list of current neighbors to scanner 0
    %terminating once the neighbor list contains all the scanners
    count1 = 1;
    while length(scanner_indices)<num_scanners
        %current neighbor that we are looking at
        neighbor_vertex = scanner_indices(count1);
        
        %transformation from neighbor frame to scanner 0 frame
        RBT_forward_neighbor = scanner_forward_transformations{neighbor_vertex};
        
        %iterate through the neighbors of the current neighbor
        reachable_vertices = my_graph_indices_list{neighbor_vertex};
        for i = 1:length(reachable_vertices)
            %current neighbor's neighbor
            reachable_vertex = reachable_vertices(i);
            
            %if we have not seen the neighbor's neighbor yet
            if sum(reachable_vertex==scanner_indices) == 0
                %transformation from neighbor's neightbor frame to neighbor frame
                RBT_forward_reachable = my_graph_forward_transformation_list{neighbor_vertex}{i};
                
                %compute the transformation from the neighbor's neighbor frame
                %to the scanner 0 frame by composing the two extracted
                %transformations, and then
                %store it in the list of transformations
                scanner_forward_transformations{reachable_vertex} = RBT_forward_neighbor*RBT_forward_reachable;
                
                %add the neighbor's neighbor to the neighbor list
                scanner_indices(end+1) = reachable_vertex;
            end
        end
        
        count1=count1+1;
    end
end

%note, they made it really easy for us in terms of resolving ambiguity in
%the problem input. my technique here exploits this
function [my_graph_forward_transformation_list,my_graph_indices_list] = build_Graph(parsed_beacon_data,dmat_list,dsignature_list,dsignature_index_list)
    num_scanners = length(parsed_beacon_data);

    %my_graph_indices_list{i} is the list of scanners that share 12 beacons
    %with the ith scanner
    my_graph_indices_list = cell(1,num_scanners);
    
    %my_graph_forward_transformation_list{i}{j} is the transformation
    %mapping the my_graph_indices_list{i}(j)'th scanner frame to the
    %ith scanner frame
    my_graph_forward_transformation_list = cell(1,num_scanners);
    
    %initialize these two list of lists as empty
    for i = 1:num_scanners
        my_graph_indices_list{i}=[];
        my_graph_forward_transformation_list{i}={};
    end
    
    %number of beacons that must overlap for two scanners to *see* each other
    min_beacon_overlap = 12;
    
    %number of distances in the bottom triangle of the distance matrices
    %(not including the diagonal of zeros)
    %that must overlap for two scanners to *see* each other
    min_distance_list_overlap = min_beacon_overlap*(min_beacon_overlap-1)/2;
    
    %4x4 identity matrix, which we use alot, so we don't want to recompute
    I4 = eye(4);
    
    %iterate through each pair of scanners (i,j), j<=i
    for i = 1:num_scanners
        for j = 1:i
            %if the two scanners are different...
            if i~=j
                %check to see if the scanners *see* each other by looking
                %at the overlap of the elements of the two distance matrices
                [num_overlap,index1_list,index2_list] = compute_list_overlap(dsignature_list{i},dsignature_list{j});
                if num_overlap>=min_distance_list_overlap
                    %if there is enough overlap...
                    
                    %identify the indices of the beacons for which the two
                    %distance matrices overlap
                    reduced_index_list1 = unique([dsignature_index_list{i}(1,index1_list),dsignature_index_list{i}(2,index1_list)]);
                    reduced_index_list2 = unique([dsignature_index_list{j}(1,index2_list),dsignature_index_list{j}(2,index2_list)]);

                    %use this to reduce the two distance matrices to the
                    %12x12 components that actually overlap
                    reduced_distance_matrix1 = dmat_list{i}(reduced_index_list1,reduced_index_list1);
                    reduced_distance_matrix2 = dmat_list{j}(reduced_index_list2,reduced_index_list2);

                    %at this point reduced_distance_matrix1 is a
                    %permutation of reduced_distance_matrix2. 
                    %we need to identify this permutation. 
                    %actually robustly solving this problem 
                    %of identify two respective submatrices of each distance
                    %matrix that matches is called the
                    %subgraph isomorphism problem which is...NP-complete
                    %thankfully, the input is friendly in an exploitable
                    %way. specifically, all the distances are close to 
                    %unique. thus, we are just going to sort each distance
                    %matrice only across the columns, and then compare
                    %which vectors match to each other. this gives us
                    %the permutation that we are looking for
                    %if the input weren't as friendly, we couldn't do this
                    %but, I guess they chose to be nice to us
                    
                    %sort each reduced distance matrix across the columns
                    sorted_reduced_distance_matrix1 = sort(reduced_distance_matrix1);
                    sorted_reduced_distance_matrix2 = sort(reduced_distance_matrix2);
                    
                    %find the permutation between the distance matrices
                    my_permutation = find_permutation(sorted_reduced_distance_matrix1,sorted_reduced_distance_matrix2);

                    coord_set1 = parsed_beacon_data{i}(:,reduced_index_list1);
                    coord_set2 = parsed_beacon_data{j}(:,reduced_index_list2(my_permutation));
                    
                    [RBT_forward,RBT_back] = compute_rigid_body_transformation(coord_set1,coord_set2);
                    if det(RBT_forward(1:3,1:3))>0
                        my_graph_forward_transformation_list{i}{end+1}=RBT_forward;
                        my_graph_indices_list{i}(end+1) = j;
                        my_graph_forward_transformation_list{j}{end+1}=RBT_back;
                        my_graph_indices_list{j}(end+1) = i;
                    end
                end
            else
                %if it's the same scanner, then the transformation to
                %itself is just the identity
                my_graph_forward_transformation_list{i}{end+1}=I4;
                my_graph_indices_list{i}(end+1) = i;
            end
        end
    end
end

%given a list of N  k-dimensional vectors (in the form of a k x N matrix)
%and its permutation (also in the form of a k x N matrix)
%find the permutation between the two lists
function my_permutation = find_permutation(V1_list,V2_list)
    num_vectors = size(V1_list,1);
    
    %permutation between the two vectors
    my_permutation = zeros(1,num_vectors);
    
    %for the ith vector in V1_list
    for i=1:num_vectors
        
        %search for the vector in V2_list that matches
        for j=1:num_vectors
            %once we have found such a vector
            if sum((V1_list(:,i)-V2_list(:,j)).^2)==0
                %we've identified the ith element of the permutation
                %update the permutation accordingly
                my_permutation(i)=j;
            end
        end
    end
end


%transform the coordinates of a set of points from frame 2 to frame 1
%using the rigid body transformation matrix between the two frames
function beacon_coords = transform_coords(beacon_coords,RBT_forward)
    beacon_coords =([eye(3),zeros(3,1)]*RBT_forward)*[beacon_coords;ones(1,size(beacon_coords,2))];
end

%Invert a rigid body transformation matrix
function RBT_back = invert_RBT(RBT_forward)
    R = RBT_forward(1:3,1:3);
    T = RBT_forward(1:3,4);
    RBT_back = build_RBT(R',-R'*T);
end

%Build a rigid body transformation matrix from a rotation and a translation
function RBT_forward = build_RBT(R,T)
    RBT_forward = [[R,T];[0,0,0,1]];
end

%computes the forward (RBT_forward) and backwards (RBT_back) rigid body transformation 
%that maps between a set of points in frame1 and frame2
%If P is a coordinate vector of a point in frame 1
%and Q is a coordinate vector of the same point in frame 2 then:
%RBT_forward*[Q;1]=[P;1] and RBT_back*[P;1]=[Q;1]
%also, RBT_forward*RBT_back is the 4x4 identity
function [RBT_forward,RBT_back] = compute_rigid_body_transformation(coord_matrix1,coord_matrix2)

    %we begin by computing the relative rotation between frames 1 & 2
    
    %to do this, we compute a set of difference vectors of the same set of
    %points in frames 1 & 2
    V1 = diff(coord_matrix1,1,2);
    V2 = diff(coord_matrix2,1,2);
    
    %Note that if R rotates vectors from frame 2 to frame 1, we get:
    %R*V2=V1
    %R*V2*V2^T=V1*V2^T
    %R=(V1*V2^T)/(V2*V2^T)
    
    %since we know that R corresponds to a combination of 90 degree
    %rotations,  we know that all elements are +/- 1 or 0
    %so we should round the result in case the inversion caused the answer
    %to slightly deviate.
    
    R = round((V1*V2')/(V2*V2'));

    %Now we compute the translation
    %If P is a coordinate vector of a point in frame 1
    %and Q is a coordinate vector of the same point in frame 2 then:
    %R*Q+T=P  -> T=P-R*Q, where T is the translation
    T = coord_matrix1(:,1)-R*coord_matrix2(:,1);

    %Once we know the translation and rotation, we can build  the 
    %rigid body transformation matrices
    RBT_forward = build_RBT(R,T);
    RBT_back = build_RBT(R',-R'*T);
end

%compute the maximum manhattan distance between any pair of scanners
function compute_max_manhattan_distance(scanner_coord_matrix)
    num_scanners = size(scanner_coord_matrix,2);
    max_manhattan_distance = 0;
    
    %iterate through every pair of different scanners
    for i = 1:num_scanners
        for j = 1:(i-1)
            %compute the manhattan distance
            %between the ith and jth scanners
            manhattan_distance = sum(abs(scanner_coord_matrix(:,i)-scanner_coord_matrix(:,j)));
            
            %if that distance is larger than what we have seen, record it
            if manhattan_distance>max_manhattan_distance
                max_manhattan_distance=manhattan_distance;
            end
        end
    end
    
    %print out the result
    disp(['max_manhattan_distance: ',num2str(max_manhattan_distance)])
end

%count the number of unique beacons, and then print the result
function compute_num_unique_beacons(coord_matrix)
    %first, sort the beacon list in lexicographic order
    coord_matrix = coord_lexicographic_sort(coord_matrix);
    
    num_beacons = size(coord_matrix,2);
    
    %if there is at least 1 beacon, then the first beacon in the list
    %counts for at least one unique beacon
    num_unique_beacons=num_beacons>0;
    
    %iterate through the list of beacons (except for the first beacon)
    for i = 2:size(coord_matrix,2)
        %if we see a different beacon then the previous
        %then increment the number of unique beacons.
        %this works because the list of beacons is sorted lexicographically
        if sum(coord_matrix(:,i)==coord_matrix(:,i-1))<3
            num_unique_beacons = num_unique_beacons+1;
        end
    end
    
    %print out the final result
    disp(['number of unique beacons: ',num2str(num_unique_beacons)]);
end

%sort a matrix of beacon coordinates in lexicographic order
%specifically, if v and w are the coordinates of two beacons,
%then v<w means that either 
%  v(1)<w(1) or
% (v(1)==w(1) && v(2)<w(2)) or
% (v(1)==w(1) && v(2)==w(2) && v(3)<w(3))
function coord_matrix = coord_lexicographic_sort(coord_matrix)
    %total number of beacons
    num_beacons=size(coord_matrix,2);

    %begin by sorting the coordinate matrix by its first index
    [~,sorted_index_list] = sort(coord_matrix(1,:));
    coord_matrix = coord_matrix(:,sorted_index_list);
    
    %sort by the second and then third indices
    for j=2:3
        
        %count1:(count2-1) corresponds to a range of indices for which
        %1:(j-1) coordinates are the same for all the beacons in the range
        count1=1;
        count2=2;
        
        %iterate through all the beacons in the list
        while count2<=num_beacons
            
            %if we see a beacon with different 1:(j-1) coordinates
            if sum(coord_matrix(1:(j-1),count2)~=coord_matrix(1:(j-1),count1))>0
                %sort the beacons in the range count1:(count2-1) 
                %by their jth coordinate
                [~,sorted_index_list] = sort(coord_matrix(j,count1:(count2-1)));
                coord_matrix(:,count1:(count2-1))=coord_matrix(:,count1-1+sorted_index_list);
                
                %reset the range
                count1=count2;
            end
            count2=count2+1;
                
        end
        
        %sort the beacons in the range count1:(count2-1) 
        %by their jth coordinate
        [~,sorted_index_list] = sort(coord_matrix(j,count1:(count2-1)));
        coord_matrix(:,count1:(count2-1))=coord_matrix(:,count1-1+sorted_index_list);
    end
end

%this function computes how many shared elements two lists have
%repeats get counted, but only if they are shared!
%as well as the list of indices that correspond to shared elements
%it is assumed that list1 and list2 are sorted in the ascending order

%num_shared_elements is the number of shared elements (lol)
%list1(index1_list(i)) = list2(index2_list(i))
function [num_shared_elements,index1_list,index2_list] = compute_list_overlap(list1,list2)
    %length of the lists
    numel1 = length(list1);
    numel2 = length(list2);

    %initialize our return data
    index1_list = [];
    index2_list = [];

    num_shared_elements = 0;

    %respective indices for interating through each of the lists
    index1=1;
    index2=1;
    
    %if we haven't reached the end of either list yet
    while index1<=numel1 && index2<=numel2
        %extract the current values of each of the lists
        v1 = list1(index1);
        v2 = list2(index2);

        %if the element is shared
        if v1 == v2
            %increment the number of shared elements counted
            num_shared_elements = num_shared_elements+1;
            
            %store the shared indices in each of the lists
            index1_list(end+1) = index1;
            index2_list(end+1) = index2;
            
            %increment the indices
            index1 = index1+1;
            index2 = index2+1;
        else
            %if elements are not shared, increment the index corresponding
            %to the smaller element (so it can catch up!)
            if v1<v2
                index1 = index1+1;
            else
                index2 = index2+1;
            end
        end
    end
end

%this function calls build_distance_matrix for each of the scanners
%and then stores the results in a cell array
function [dmat_list,dsignature_list,dsignature_index_list] = build_all_distance_information(parsed_beacon_data,num_scanners)
    dmat_list = cell(1,num_scanners);
    dsignature_list = cell(1,num_scanners);
    dsignature_index_list = cell(1,num_scanners);
    for i = 1:num_scanners
        [distance_matrix,distance_list,vertex_index_list] = build_distance_matrix(parsed_beacon_data{i});
        dmat_list{i} = distance_matrix;
        dsignature_list{i} = distance_list;
        dsignature_index_list{i} = vertex_index_list;
    end
end

%compute the pairwise squared distance matrix for a set of beacons
%specifically distance_matrix(i,j) is equal to the squared distance between
%the ith and jth beacons
%this function also returns the same distance matrix in list form
%with a list of the corresponding paired indices. specifically
%distance_list(i) is the distance between 
%the beacon_index_list(1,i)th and beacon_index_list(2,i)th beacons
function [distance_matrix,distance_list,beacon_index_list] = build_distance_matrix(coord_matrix)
    %find the total number of  beacons we are looking at
    num_beacons = size(coord_matrix,2);
    
    %initialize the pairwise squared distance matrix
    %as well as the distance and index lists
    distance_matrix = zeros(num_beacons,num_beacons);
    distance_list = zeros(1,num_beacons*(num_beacons-1)/2);
    beacon_index_list = zeros(2,num_beacons*(num_beacons-1)/2);
    
    %index for storing information in distance_list and beacon_index_list
    distance_index = 1;
    
    %iterate through all pairs of beacons (i,j) where j<i note that:
    %1. since the distance from beacon i to itself is 0
    %we've already correctly initialize all distance_matrix(i,i)
    %thus no reason to iterate through i==j
    %2. the distance matrix is symmetric, so we can set
    %distance_matrix(i,j) and distance_matrix(j,i) at the same time
    %thus, no reason to iterate through i<j
    for i = 1:num_beacons
        for j = 1:(i-1)
            
            %compute the squared distance between becomes i and j
            distance_squared = sum((coord_matrix(:,i)-coord_matrix(:,j)).^2);
            
            %store it in the distance matrix (which is symmetric)
            distance_matrix(i,j) = distance_squared;
            distance_matrix(j,i) = distance_squared;

            %store it in the distance list as well, and record the pairs
            %of indices that we are storing
            distance_list(distance_index)=distance_squared;
            beacon_index_list(1,distance_index)=i;
            beacon_index_list(2,distance_index)=j;
            
            distance_index = distance_index+1;
        end
    end
    %sort the distance list, and shuffle the indices so they match the 
    %sorted list
    [distance_list,sorted_indices] = sort(distance_list);
    beacon_index_list = beacon_index_list(:,sorted_indices);
end

function [parsed_beacon_data,num_scanners]=parse_data_file()
    %step 1: parse the input
    fid = fopen('InputDay19.txt');

    %extract text, splitting it by line
    data = textscan(fid,'%s','Delimiter','/');
    data = data{1};
    fclose(fid);

    %number of lines of text in the file
    file_length = length(data);

    %parsed_beacon_data{i+1} is the beacon coordinate information matrix
    %for the ith scanner. Specifically, if parsed_beacon_data{i+1} = M
    %M(j,k) is the jth coordinate of the kth beacon as seen by the ith scanner 
    parsed_beacon_data = {};
    
    %total number of scanners
    num_scanners = 0;
    
    %current input line when reading file
    input_line = 1;
    
    %beacon coordinate matrix for each scanner
    coord_matrix = [];
    
    %iterate through every file in the input
    while input_line <= file_length
        
        %read the current line of text in the file
        input_string = data{input_line};
        
        %if the line of text contains the substring 'scanner'
        %then we are starting to parse the information for the next scanner
        if contains(input_string,'scanner')
            %if we have recorded information so far
            %then store the recorded information in our lists
            if num_scanners>0
                parsed_beacon_data{num_scanners} = coord_matrix;
            end
            
            %increment the number of scanners
            num_scanners = num_scanners+1;
            
            %reset the beacon data
            coord_matrix = [];
        else
            %In this case, we are looking at a line of beacon data
            
            %convert the input string to a column vector
            %and append it to the end of the coordinate matrix
            coord_matrix = [coord_matrix,str2num(input_string)'];
        end

        %go to the next line of the file
        input_line = input_line+1;
    end
    %store the recorded information of the last scanner in our lists
    parsed_beacon_data{num_scanners} = coord_matrix;
end