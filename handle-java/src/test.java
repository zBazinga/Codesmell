import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.EOFException;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;



public class test {
    // 改变项目名称即可
    public static void main(String[] args) throws IOException {
        String project = "californium-master";
        String all_path = "/Users/dashabi/Desktop/MoveMethodGenerator-master/data/";
        String csv_path = all_path+project+"/classes.csv";
        BufferedReader reader = new BufferedReader(new FileReader(csv_path));
        reader.readLine();
        String line = null;
        while((line=reader.readLine())!=null){
            String item[] = line.split(",");
            //System.out.println(item.length);
            String last = item[item.length-1];
            String class_name_pre[] = item[1].split("[.]");
            String class_name = class_name_pre[class_name_pre.length-1];
            //System.out.println(class_name);
            String project_name ="/Users/dashabi/Desktop/MoveMethodGenerator-master/data-project/"+project+"/";
            String path = project_name+item[2];
            //System.out.println(path);
            DemoVisitorTest result = new DemoVisitorTest(path);
            //System.out.println(test.result_pre.size());
            //System.out.println(test.result_pre);
            String text = "/Users/dashabi/Desktop/data-text/";
            String text_file_store = text+project;
            String text_store = text_file_store+"/"+class_name+".txt";
            File f=new File(text_file_store);
            if(!f.exists())
            {
                f.mkdirs();
            }
            File f2 = new File(text_store);
            FileWriter fw;
            fw=new FileWriter(f2);
            for(int i = 0; i< result.result_pre.size();i++)
            {
                String str= result.result_pre.get(i)+"\n";
                fw.write(str);
            }

            fw.close();

        }

    }
}