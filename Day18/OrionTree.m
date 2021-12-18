classdef OrionTree < handle
    properties
        left_child;
        right_child;
    end
    
    methods
        function obj = OrionTree(left_child,right_child)
            obj.left_child = left_child;
            obj.right_child = right_child;
        end
        
        function setLeft(obj,left_child)
            obj.left_child = left_child;
        end
        
        function setRight(obj,right_child)
            obj.right_child = right_child;
        end
        
        function left_child = getLeft(obj)
            left_child = obj.left_child;
        end
        
        function right_child = getRight(obj)
            right_child = obj.right_child;
        end
    end
end