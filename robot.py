import wpilib as wpi
from enums import XboxButton


class MyRobot (wpi.IterativeRobot):
    frontLeftChannel  = 0
    rearLeftChannel   = 1
    frontRightChannel  = 2
    rearRightChannel   = 3

    joystickChannel  = 0

    solenoidChannel = 0

    gyroChannel = 0 #wpi.SPI.Port.kOnboardCS0

    sparkChannel = 4

    def robotInit(self):
        self.timer = wpi.Timer()

        self.deltaTime = 0
#        self.motors = [wpi.Spark(x) for x in range(4)]

        self.drive = wpi.RobotDrive(wpi.Spark(0), wpi.Spark(1),
                                    wpi.Spark(2), wpi.Spark(3))#self.motors[MyRobot.frontLeftChannel],
                                    #self.motors[MyRobot.rearLeftChannel],
                                    #self.motors[MyRobot.frontRightChannel],
                                    #self.motors[MyRobot.rearRightChannel])
        self.joystick = wpi.XboxController(MyRobot.joystickChannel)
        self.solenoid = wpi.Solenoid(MyRobot.solenoidChannel)
        self.gyro = wpi.AnalogGyro(MyRobot.gyroChannel)
        self.gyro.calibrate()
        #self.auto_cntr = 0
        self.auto_state = 0

        self.auto_chooser = wpi.SendableChooser()
        self.auto_chooser.addObject("Left", 1)
        self.auto_chooser.addObject("Center", 2)
        self.auto_chooser.addObject("Right", 3)
        wpi.SmartDashboard.putData("Autonomouse Position", self.auto_chooser)



        self.solenoid.set(False)

        self.drivestate = False

    def autonomousInit(self):
        self.auto_state = self.auto_chooser.getSelected()
        self.gyro.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        #Middle One second at half speed = 8ft
        wpi.DriverStation.reportWarning(str(self.gyro.getAngle()), False)
        #if self.timer.get() < 1.104:
            #self.drive.mecanumDrive_Cartesian(0, 0, 1*.5, self.gyro.getAngle())
        if self.timer.get() < .57:
            self.drive.mecanumDrive_Cartesian(0, -1*.25, 0, self.gyro.getAngle())
        #elif self.timer.get() < 8.4:
            #self.drive.mecanumDrive_Cartesian(0, 0, 0, self.gyro.getAngle())
        #elif self.timer.get() < 9:
            #self.drive.mecanumDrive_Cartesian(0, 0, -1*.5, self.gyro.getAngle())
        #else:
            #self.drive.mecanumDrive_Cartesian(0, 0, 0, self.gyro.getAngle())




        #Left/Right
        #self.mecanumDrive_Cartesian(0, 3.5*.5, 0, self.gyro.getAngle())
        #self.mecanumDrive_Cartesian(0, 3.5*.5, 0, self.gyro.getAngle()



    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        wpi.DriverStation.reportWarning(str(self.gyro.getAngle()), False)
        lefty = -self.joystick.getY(wpi.GenericHID.Hand.kLeft)
        leftx = self.joystick.getX(wpi.GenericHID.Hand.kLeft)
        rightx = self.joystick.getX(wpi.GenericHID.Hand.kRight)

        if lefty < 0.25 and lefty > -0.25:
            lefty = 0
        if rightx < 0.25 and rightx > -0.25:
            rightx = 0
        if leftx < 0.25 and leftx > -0.25:
            leftx = 0


        #self.drive.mecanumDrive_Cartesian(-leftx/2, -rightx/2, -lefty/2)

        #self.drive.mecanumDrive_Cartesian(-leftx, -rightx, lefty, 0)
        if self.joystick.getAButton():
            state = self.solenoid.get()
            if state == False:
                self.solenoid.set(True)
            else:
                self.solenoid.set(False)
        if self.joystick.getYButton():
            if self.drivestate:
                self.drivestate = False
            else:
                self.drivestate = True


        if self.drivestate == True:
            rightx = rightx / 2
            lefty = lefty / 2
            leftx = leftx / 2

        self.drive.mecanumDrive_Cartesian(-leftx, -rightx, lefty, 0)





if __name__ == '__main__':
    wpi.run(MyRobot)