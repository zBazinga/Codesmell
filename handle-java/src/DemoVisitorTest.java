import org.eclipse.jdt.core.dom.CompilationUnit;

import java.util.ArrayList;
import java.util.List;

public class DemoVisitorTest {
    public List<String> result_pre = new ArrayList<>();
    public DemoVisitorTest(String path) {
        CompilationUnit comp = JdtAstUtil.getCompilationUnit(path);
        DemoVisitor visitor = new DemoVisitor();
        result_pre=visitor.result;
        comp.accept(visitor);
    }


}
