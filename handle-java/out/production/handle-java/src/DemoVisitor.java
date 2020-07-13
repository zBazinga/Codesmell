import org.eclipse.jdt.core.dom.*;

import java.util.*;

public class DemoVisitor extends ASTVisitor {
    public List<String> result = new ArrayList<>();
    @Override
    public boolean visit(FieldDeclaration node) {
        for (Object obj: node.fragments()) {
            VariableDeclarationFragment v = (VariableDeclarationFragment)obj;
            String mid = v.getName().toString();
            String mid2 = "Field:"+mid;
            result.add(mid2);
            //System.out.println("Field:\t" + v.getName());
        }

        return true;
    }

    @Override
    public boolean visit(MethodDeclaration node) {

//        System.out.println("Method-name:\t" + node.getName()); // ????
//        System.out.println("Method-returnType:\t" + node.getReturnType2()); // ??????
//        System.out.println("Method-parameters:\t" + node.parameters()); // ??
        String mid1 = "Method-name:"+node.getName().toString();
        String mid2 = "Method-returnType:"+node.getReturnType2();
        String mid3 = "Method-parameters:"+node.parameters().toString();
        result.add(mid1);
        result.add(mid2);
        result.add(mid3);
        return true;
    }

    @Override
    public boolean visit(TypeDeclaration node) {
        if(!node.isInterface())
        {
            String mid1 = "Class:"+node.getName().toString();
            result.add(mid1);
            //System.out.println("Class:\t" + node.getName());
        }

        return true;
    }

    @Override
    public boolean visit(MethodInvocation node) {
        String mid1 = "MethodInvocation:"+node.getName().toString();
        result.add(mid1);
        //System.out.println("MethodInvocation:\t" + node.getName());
        //System.out.println("MethodInvocation:\t" + node.get);
        return true;
    }

    @Override
    public boolean visit(FieldAccess  node) { // ????????,???????????????
        String mid1 = "FieldAccess:"+node.getName().toString();
        result.add(mid1);
        //System.out.println("FieldAccess :\t" + node.getName()); //?????????????
        return true;
    }


}


