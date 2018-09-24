// Adder DUT
module filter (data, out1, out2, out3, clk, rst);
  input      [1:0] data;
  input      clk;
  input      rst;
  output    [11:0] out1;
  output    [11:0] out2;
  output    [11:0] out3;

  wire data;

  //reg signed [7:0] d1;
  reg [64:0] buffer1;
  reg [30:0] buffer2;
  reg [40:0] buffer3;
  reg signed [7:0] d2;
  //reg signed [7:0] d3;
  reg signed [9:0] d4;
  //reg signed [11:0] d5;
  reg signed [11:0] d6;
  reg [7:0] counter;

  always @(posedge clk)
	begin
		if (rst)
      begin
        counter <= 0;
        buffer1 <= 0;
        buffer2 <= 0;
        buffer3 <= 0;
  			//d1 <= 0;
  			d2 <= 0;
  			//d3 <= 0;
  			d4 <= 0;
  			//d5 <= 0;
  			d6 <= 0;
      end else begin
        counter <= counter + 1;
        buffer1[0] = data;
        buffer1 <= buffer1 << 1;
        //d1 <= data - buffer1[63]; // L = 63
  			d2 <= d2 + data - buffer1[63];
        if (counter[3])
          begin  // D = 8
            buffer2[5:0] = d2;
            buffer2 <= buffer2 << 6;  //0-64 input width
            //d3 <= d2 - buffer2[29:24]; // L = 4
            d4 <= d4 + d2 - buffer2[29:24];

            buffer3[7:0] = d4;
            buffer3 <= buffer3 << 8;  //0-256 input width
            //d5 <= d4 - buffer3[39:32]; // L = 4
            d6 <= d6 + d4 - buffer3[39:32];

            counter <= 0;
          end
        end
    end

    assign out1 = d2;
    assign out2 = d4;
    assign out3 = d6;

endmodule
