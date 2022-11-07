function res=submarine01()

%target area: x=56..76, y=-162..-134

x_range = [56,76];
y_range = [-162,-134];
x_start = 0;
y_start = 0;


% dy = abs(diff(y_range))

%step 1: find the minimum x velocity to pass through x_range

a = .5;
b = .5;
c = -x_range(1);




vx_min = ceil(-b+sqrt(b^2-4*a*c))/(2*a);


vx_max = 76;

max_turns = 1+2*161;
min_turns = 1;

vx_range = vx_min:vx_max;
vy_range = -162:161;


vx_turn_range = [max_turns*ones(1,length(vx_range));min_turns*ones(1,length(vx_range))];
vy_turn_range = [max_turns*ones(1,length(vy_range));min_turns*ones(1,length(vy_range))];


count = 1;

for i = vx_range
    x_path = cumsum([[i:-1:0],zeros(1,max_turns+1-i)]);
    possible_turns = find((x_range(1)<=x_path).*(x_path<=x_range(2)));
    
    if length(possible_turns)>0
        vx_turn_range(1,count)=min(possible_turns);
        vx_turn_range(2,count)=max(possible_turns);
    else
        vx_turn_range(1,count)=max_turns;
        vx_turn_range(2,count)=-1;
    end
    count = count+1;
end

count = 1;
for i = vy_range
    y_path = cumsum([i:-1:-max_turns]);
    possible_turns = find((y_range(1)<=y_path).*(y_path<=y_range(2)));
    
    if length(possible_turns)>0
        vy_turn_range(1,count)=min(possible_turns);
        vy_turn_range(2,count)=max(possible_turns);
    else
        vy_turn_range(1,count)=max_turns;
        vy_turn_range(2,count)=-1;
    end
    count = count+1;
end

count = 0;

for i = 1:length(vx_range)
   for j = 1:length(vy_range)
        if vx_turn_range(1,i)<=vy_turn_range(2,j) && vy_turn_range(1,j)<=vx_turn_range(2,i)
            count = count+1;
        end
   end
end
count
% 
% (161*162)/2
end


