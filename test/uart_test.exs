defmodule UartTest do
  use ExUnit.Case
  doctest Uart

  test "greets the world" do
    assert Uart.hello() == :world
  end
end
