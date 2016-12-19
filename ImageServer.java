import java.net.ServerSocket;
import java.net.Socket;
import java.io.InputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.File;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
public class ImageServer extends java.lang.Thread{
	private ServerSocket server;
	private final int ServerPort = 8000;
	public ImageServer(){
		try{
			server = new ServerSocket(ServerPort);
		}
		catch(java.io.IOException e){
			System.out.println(e.toString());
		}
	}

	public void run(){
		Socket socket;

		System.out.println("Image Server Started");
		while(true){
			socket = null;
            try {
                synchronized (server) {
                    socket = server.accept();
                }
                System.out.println("Get Connection : InetAddress = " + socket.getInetAddress());
                // TimeOut Time
                socket.setSoTimeout(15000);
                DataInputStream in = new DataInputStream(socket.getInputStream());
				int fileCount = 0;
				while(true){
					byte[] intBuffer = new byte[4];
					in.read(intBuffer);
					//int image_len = in.readInt();
					ByteBuffer bb = ByteBuffer.wrap(intBuffer);
					bb.order(ByteOrder.LITTLE_ENDIAN);
					int image_len = bb.getInt();
					System.out.println("Image Length: "+image_len);
					if(image_len ==0 ) break;
					fileCount++;
					File file = new File("image"+fileCount+".jpg");
					file.createNewFile();
				    DataOutputStream dos = new DataOutputStream(new FileOutputStream(file));
				    int count;
				    byte[] buffer = new byte[image_len];
			        in.read(buffer, 0, image_len);
				    //while ((count = in.read(buffer)) > 0)
				    //{
					      dos.write(buffer, 0, image_len);
					      dos.flush();
				    //}
				    dos.close();
			    	System.out.println("image transfer done");
				}
			    socket.close();     
 
            } catch (java.io.IOException e) {
                System.out.println("Socket Connection Error !");
                System.out.println("IOException :" + e.toString());
            }
            catch(Exception e){ 
            }
		}
	}
	public static void main(String[] args){
		(new ImageServer()).start();
	}
}
