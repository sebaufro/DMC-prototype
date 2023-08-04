//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#pragma once

module ManagerRef
{
	exception notFoundRef
    {
        string reason = "Reference not found";
    }
    exception notFoundClass
    {
        string reason = "Class not found";
    }
    interface Manager
    {
    	int addRef(string name, string origin, string clsname, string descriptionpath, bool protected);
        string findRefByName(string name) throws notFoundRef;
        string findRefsDefs(string name) throws notFoundRef;
        int addObjToServer(string compName, string clsName) throws notFoundClass;

        void shutdown();
    }

    
}


